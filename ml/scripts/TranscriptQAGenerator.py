# Enhanced TranscriptQAGenerator.py - Updated with all improvements

import torch
from transformers import T5ForConditionalGeneration, T5Tokenizer, pipeline
from typing import List, Dict, Any, Tuple
import re
import nltk
from sentence_transformers import SentenceTransformer, util
import random
import spacy
import logging
from collections import defaultdict
import json
from datetime import datetime

# Configure logging to see the generation process and diagnose issues
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class TranscriptQAGenerator:
    """
    Enhanced ML Model for generating high-quality, semantically unique, and fact-checked
    MCQ Question-Answer pairs from input transcripts.
    
    Major improvements:
    - Better models (T5-base, RoBERTa-based QA)
    - Semantic chunking instead of fixed-size chunks  
    - Answer highlighting technique for controlled QG
    - Multi-strategy distractor generation
    - Comprehensive quality validation
    - Advanced preprocessing and cleaning
    """
    
    def __init__(self, model_name: str = "valhalla/t5-base-qa-qg-hl"):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        print(f"Using device: {self.device}")
        
        # --- Enhanced Question Generation Model (upgraded to base) ---
        print("Loading Question Generation model (T5-base)...")
        self.qg_tokenizer = T5Tokenizer.from_pretrained(model_name)
        self.qg_model = T5ForConditionalGeneration.from_pretrained(model_name).to(self.device)
        
        # --- Enhanced Question Answering Model (upgraded to RoBERTa) ---  
        print("Loading Question Answering model (RoBERTa-based)...")
        self.qa_pipeline = pipeline(
            "question-answering", 
            model="deepset/roberta-base-squad2",
            tokenizer="deepset/roberta-base-squad2",
            device=0 if torch.cuda.is_available() else -1
        )
        
        # --- Model for Semantic Similarity ---
        print("Loading Semantic Similarity model...")
        self.semantic_model = SentenceTransformer('all-MiniLM-L6-v2', device=self.device)
        
        # --- Model for Named Entity Recognition (enhanced) ---
        print("Loading spaCy NER model...")
        try:
            self.ner_model = spacy.load("en_core_web_sm")
        except OSError:
            print("Downloading 'en_core_web_sm' for spaCy...")
            from spacy.cli import download
            download("en_core_web_sm")
            self.ner_model = spacy.load("en_core_web_sm")

        # --- NLTK for sentence tokenization ---
        try:
            nltk.data.find('tokenizers/punkt')
        except LookupError:
            print("Downloading NLTK punkt tokenizer...")
            nltk.download('punkt')
        
        self.is_loaded = True
        print("✅ All enhanced models initialized successfully!")
    
    def clean_transcript(self, transcript: str) -> str:
        """
        Advanced cleaning of transcript text
        """
        # Remove timestamps and speaker tags
        transcript = re.sub(r'\d{1,2}:\d{2}(:\d{2})?', '', transcript)
        transcript = re.sub(r'Speaker \d+:', '', transcript, flags=re.IGNORECASE)
        transcript = re.sub(r'\[.*?\]', '', transcript)  # Remove bracketed content
        
        # Remove filler words and hesitations
        fillers = ['um', 'uh', 'er', 'ah', 'like', 'you know', 'so', 'well']
        for filler in fillers:
            transcript = re.sub(rf'\b{filler}\b', '', transcript, flags=re.IGNORECASE)
            
        # Clean up extra whitespace and punctuation
        transcript = re.sub(r'\s+', ' ', transcript)
        transcript = re.sub(r'[,]{2,}', ',', transcript)
        transcript = re.sub(r'[.]{2,}', '.', transcript)
        
        return transcript.strip()

    def preprocess_transcript(self, transcript: str, max_chunk_size: int = 200, 
                            similarity_threshold: float = 0.7) -> List[str]:
        """
        Enhanced preprocessing with semantic chunking instead of fixed-size chunks
        """
        # First clean the transcript
        cleaned_transcript = self.clean_transcript(transcript)
        
        sentences = nltk.sent_tokenize(cleaned_transcript)
        if len(sentences) <= 1:
            return [cleaned_transcript] if len(cleaned_transcript.split()) > 20 else []
            
        # Get embeddings for all sentences for semantic chunking
        try:
            embeddings = self.semantic_model.encode(sentences)
        except Exception as e:
            logging.warning(f"Error in semantic encoding, falling back to simple chunking: {e}")
            # Fallback to simple chunking
            chunks = []
            for i in range(0, len(sentences), 3):
                chunk = ' '.join(sentences[i:i + 5])
                if len(chunk.split()) > 20:
                    chunks.append(chunk)
            return chunks
        
        # Semantic chunking based on sentence similarity
        chunks = []
        current_chunk = [sentences[0]]
        
        for i in range(1, len(sentences)):
            # Calculate similarity with current chunk
            if current_chunk:
                chunk_text = ' '.join(current_chunk)
                chunk_embedding = self.semantic_model.encode(chunk_text)
                sentence_embedding = embeddings[i]
                
                similarity = util.cos_sim(
                    torch.tensor(chunk_embedding).unsqueeze(0), 
                    torch.tensor(sentence_embedding).unsqueeze(0)
                ).item()
                
                # Check if adding this sentence exceeds size limit
                potential_chunk = ' '.join(current_chunk + [sentences[i]])
                
                if similarity > similarity_threshold and len(potential_chunk.split()) < max_chunk_size:
                    current_chunk.append(sentences[i])
                else:
                    # Start new chunk
                    if len(' '.join(current_chunk).split()) > 20:  # Minimum chunk size
                        chunks.append(' '.join(current_chunk))
                    current_chunk = [sentences[i]]
        
        # Add final chunk
        if current_chunk and len(' '.join(current_chunk).split()) > 20:
            chunks.append(' '.join(current_chunk))
            
        return chunks

    def extract_key_information(self, chunks: List[str], top_k: int = 15) -> List[str]:
        """Enhanced key information extraction"""
        if not chunks: 
            return []
        if len(chunks) <= top_k: 
            return chunks
        
        try:
            embeddings = self.semantic_model.encode(chunks, convert_to_tensor=True)
            cosine_scores = util.cos_sim(embeddings, embeddings)
            centrality_scores = cosine_scores.mean(axis=1)
            
            # Select top k most central chunks
            top_indices = torch.topk(centrality_scores, k=min(top_k, len(chunks))).indices
            return [chunks[i] for i in sorted(top_indices.tolist())]
        except Exception as e:
            logging.warning(f"Error in key information extraction: {e}")
            return chunks[:top_k]  # Fallback

    def extract_key_phrases(self, text: str) -> List[str]:
        """
        Extract important phrases and entities for answer candidates
        """
        doc = self.ner_model(text)
        
        # Extract named entities
        entities = [ent.text for ent in doc.ents if len(ent.text.split()) <= 4]
        
        # Extract noun phrases
        noun_phrases = [chunk.text for chunk in doc.noun_chunks 
                       if 2 <= len(chunk.text.split()) <= 5]
        
        # Extract important single words (proper nouns, numbers)
        important_words = [token.text for token in doc 
                          if (token.pos_ in ['PROPN', 'NUM'] or token.ent_type_) 
                          and len(token.text) > 2]
        
        # Combine and deduplicate
        key_phrases = list(set(entities + noun_phrases + important_words))
        
        # Filter by length and quality
        filtered_phrases = [phrase for phrase in key_phrases 
                          if 2 <= len(phrase) <= 50 and not phrase.isspace()]
        
        return filtered_phrases[:15]  # Limit to top 15

    def generate_questions_with_highlights(self, context: str, answer_phrases: List[str], 
                                         num_questions: int = 2) -> List[Dict[str, Any]]:
        """
        Enhanced question generation using answer highlighting technique
        """
        questions_with_answers = []
        
        for answer in answer_phrases[:min(len(answer_phrases), num_questions * 2)]:
            if answer.lower() not in context.lower():
                continue
                
            # Create highlighted context for T5 model
            highlighted_context = context.replace(
                answer, f"<hl>{answer}<hl>", 1
            )
            
            input_text = f"generate question: {highlighted_context}"
            
            try:
                # Tokenize input
                input_ids = self.qg_tokenizer.encode(
                    input_text, 
                    return_tensors="pt", 
                    max_length=512, 
                    truncation=True
                ).to(self.device)
                
                # Generate question with improved parameters
                outputs = self.qg_model.generate(
                    input_ids,
                    max_length=64,
                    num_beams=4,
                    early_stopping=True,
                    no_repeat_ngram_size=3,
                    temperature=0.8,
                    do_sample=True,
                    pad_token_id=self.qg_tokenizer.eos_token_id
                )
                
                question = self.qg_tokenizer.decode(
                    outputs[0], skip_special_tokens=True
                )
                
                # Clean the question
                question = self.clean_question(question)
                
                if self.is_valid_question(question, context, answer):
                    questions_with_answers.append({
                        'question': question,
                        'answer': answer,
                        'context': context
                    })
                    
                    if len(questions_with_answers) >= num_questions:
                        break
                        
            except Exception as e:
                logging.warning(f"Error generating question for answer '{answer}': {e}")
                continue
        
        return questions_with_answers

    def clean_question(self, question: str) -> str:
        """Clean and format generated questions"""
        # Remove any artifacts from generation
        question = question.replace("generate question:", "").strip()
        question = question.replace("<hl>", "").replace("</hl>", "")
        
        # Ensure proper capitalization
        if question:
            question = question[0].upper() + question[1:]
            
        # Ensure question ends with ?
        if question and not question.endswith('?'):
            question += '?'
            
        return question

    def is_valid_question(self, question: str, context: str, expected_answer: str) -> bool:
        """Validate if the generated question is good quality"""
        if not question or len(question.split()) < 4:
            return False
            
        if not question.endswith('?'):
            return False
            
        # Check if question is answerable with expected answer
        try:
            qa_result = self.qa_pipeline(question=question, context=context)
            predicted_answer = qa_result['answer'].lower()
            expected_lower = expected_answer.lower()
            
            # Check if predicted answer matches or is contained in expected answer
            if (predicted_answer in expected_lower or 
                expected_lower in predicted_answer or
                qa_result['score'] > 0.3):
                return True
                
        except Exception:
            pass
            
        return False

    def analyze_answer_type(self, answer: str) -> Dict[str, Any]:
        """Analyze the answer to determine its type and characteristics"""
        doc = self.ner_model(answer)
        
        analysis = {
            'text': answer,
            'entity_type': None,
            'pos_tags': [token.pos_ for token in doc],
            'is_numeric': any(token.like_num for token in doc),
            'is_proper_noun': any(token.pos_ == 'PROPN' for token in doc),
            'length': len(answer.split()),
            'entities': [(ent.text, ent.label_) for ent in doc.ents]
        }
        
        # Determine primary entity type
        if doc.ents:
            analysis['entity_type'] = doc.ents[0].label_
        elif analysis['is_numeric']:
            analysis['entity_type'] = 'CARDINAL'
        elif analysis['is_proper_noun']:
            analysis['entity_type'] = 'PROPN'
        else:
            analysis['entity_type'] = 'NOUN'
            
        return analysis

    def extract_entities_by_type(self, context: str, full_transcript: str = None) -> Dict[str, List[str]]:
        """Extract entities from context, organized by type"""
        entities_by_type = defaultdict(list)
        
        # Process main context
        doc = self.ner_model(context)
        for ent in doc.ents:
            if len(ent.text.strip()) > 1 and not ent.text.strip().isdigit():
                entities_by_type[ent.label_].append(ent.text.strip())
        
        # Process full transcript if available for more diverse distractors
        if full_transcript and full_transcript != context:
            doc_full = self.ner_model(full_transcript)
            for ent in doc_full.ents:
                if len(ent.text.strip()) > 1 and not ent.text.strip().isdigit():
                    entities_by_type[ent.label_].append(ent.text.strip())
        
        # Deduplicate
        for entity_type in entities_by_type:
            entities_by_type[entity_type] = list(set(entities_by_type[entity_type]))
            
        return dict(entities_by_type)

    def generate_numeric_distractors(self, correct_answer: str) -> List[str]:
        """Generate plausible numeric distractors"""
        distractors = []
        
        # Extract numbers from the answer
        numbers = re.findall(r'\d+(?:\.\d+)?', correct_answer)
        
        if numbers:
            base_num = float(numbers[0])
            
            # Generate variations
            variations = [
                base_num * 0.5,    # Half
                base_num * 1.5,    # 1.5x
                base_num * 2,      # Double
                base_num + 1,      # +1
                base_num - 1,      # -1
            ]
            
            for var in variations:
                if var > 0 and var != base_num:
                    # Replace original number with variation
                    new_answer = correct_answer.replace(numbers[0], str(int(var) if var.is_integer() else var))
                    distractors.append(new_answer)
        
        return distractors[:3]

    def generate_semantic_distractors(self, correct_answer: str, context: str, 
                                    full_transcript: str = None, num_distractors: int = 3) -> List[str]:
        """Enhanced multi-strategy distractor generation"""
        
        # Get all entities organized by type
        all_entities_by_type = self.extract_entities_by_type(context, full_transcript)
        answer_analysis = self.analyze_answer_type(correct_answer)
        answer_type = answer_analysis['entity_type']
        
        candidate_pool = []
        
        # Strategy 1: Same entity type distractors
        if answer_type and answer_type in all_entities_by_type:
            type_candidates = [
                ent for ent in all_entities_by_type[answer_type] 
                if ent.lower() != correct_answer.lower()
            ]
            candidate_pool.extend(type_candidates)
        
        # Strategy 2: Semantic similarity distractors
        if len(candidate_pool) < num_distractors * 2:
            all_entities = []
            for ent_list in all_entities_by_type.values():
                all_entities.extend(ent_list)
            
            if all_entities:
                try:
                    # Get semantically similar entities
                    answer_embedding = self.semantic_model.encode(correct_answer, convert_to_tensor=True)
                    candidate_embeddings = self.semantic_model.encode(all_entities, convert_to_tensor=True)
                    
                    similarities = util.cos_sim(answer_embedding, candidate_embeddings)[0]
                    
                    # Get moderately similar items (not too similar, not too different)
                    similarity_scores = [(i, score.item()) for i, score in enumerate(similarities)]
                    similarity_scores.sort(key=lambda x: x[1], reverse=True)
                    
                    for i, score in similarity_scores:
                        if 0.2 < score < 0.8:  # Sweet spot for distractors
                            entity = all_entities[i]
                            if entity.lower() != correct_answer.lower():
                                candidate_pool.append(entity)
                except Exception as e:
                    logging.warning(f"Error in semantic distractor generation: {e}")
        
        # Strategy 3: Generate numeric distractors if answer is numeric
        if answer_analysis['is_numeric'] and len(candidate_pool) < num_distractors:
            numeric_distractors = self.generate_numeric_distractors(correct_answer)
            candidate_pool.extend(numeric_distractors)
        
        # Remove duplicates and correct answer
        unique_distractors = []
        seen = set()
        for dist in candidate_pool:
            if (dist.lower() not in seen and 
                dist.lower() != correct_answer.lower() and 
                len(dist.strip()) > 0):
                unique_distractors.append(dist)
                seen.add(dist.lower())
        
        # Return top distractors, shuffled
        selected = unique_distractors[:num_distractors * 2]  # Get extra for filtering
        random.shuffle(selected)
        
        return selected[:num_distractors]

    def validate_distractors(self, question: str, correct_answer: str, 
                           distractors: List[str]) -> List[str]:
        """Validate that distractors are plausible but incorrect"""
        valid_distractors = []
        
        for distractor in distractors:
            # Basic checks
            if len(distractor.strip()) == 0:
                continue
                
            if distractor.lower() == correct_answer.lower():
                continue
            
            # Check if distractor appears in question (too obvious)
            if distractor.lower() in question.lower():
                continue
            
            # Check reasonable length similarity
            len_ratio = len(distractor) / len(correct_answer) if len(correct_answer) > 0 else 0
            if not (0.3 <= len_ratio <= 3.0):
                continue
                
            valid_distractors.append(distractor)
        
        return valid_distractors

    def estimate_difficulty(self, question: str, answer: str, distractors: List[str]) -> str:
        """Estimate difficulty level of the MCQ"""
        difficulty_score = 0
        
        # Question complexity
        question_words = len(question.split())
        if question_words > 15:
            difficulty_score += 2
        elif question_words > 10:
            difficulty_score += 1
        
        # Answer complexity
        if len(answer.split()) > 3:
            difficulty_score += 1
        
        # Distractor quality
        if len(distractors) >= 3:
            difficulty_score += 1
        
        # Question type complexity
        if any(word in question.lower() for word in ['why', 'how', 'analyze', 'compare']):
            difficulty_score += 2
        elif any(word in question.lower() for word in ['what', 'when', 'where', 'who']):
            difficulty_score += 0
        
        if difficulty_score <= 2:
            return 'Easy'
        elif difficulty_score <= 4:
            return 'Medium'
        else:
            return 'Hard'

    def classify_question_type(self, question: str) -> str:
        """Classify the type of question"""
        question_lower = question.lower()
        
        if question_lower.startswith('what'):
            return 'Factual'
        elif question_lower.startswith('when'):
            return 'Temporal'
        elif question_lower.startswith('where'):
            return 'Spatial'
        elif question_lower.startswith('who'):
            return 'Person'
        elif question_lower.startswith('why'):
            return 'Causal'
        elif question_lower.startswith('how'):
            return 'Process'
        else:
            return 'General'

    def generate_qa_pairs(self, transcript: str, max_mcqs: int = 10, min_distractors: int = 2) -> List[Dict[str, Any]]:
        """
        Main method to generate enhanced MCQs from transcript
        """
        if not self.is_loaded:
            raise RuntimeError("Models are not properly loaded.")
        
        logging.info(f"Starting enhanced MCQ generation for transcript of {len(transcript)} characters")
        
        # Enhanced preprocessing with semantic chunking
        chunks = self.preprocess_transcript(transcript)
        if not chunks:
            logging.warning("Preprocessing returned no chunks from the transcript.")
            return []
        
        logging.info(f"Created {len(chunks)} semantic chunks")
        
        # Extract key information
        key_chunks = self.extract_key_information(chunks, top_k=min(15, len(chunks)))
        
        all_mcqs = []
        seen_question_embeddings = []
        
        # Get all entities from full transcript for better distractors
        cleaned_full_transcript = self.clean_transcript(transcript)

        for i, chunk in enumerate(key_chunks):
            if len(all_mcqs) >= max_mcqs:
                break
                
            logging.info(f"--- Processing Chunk {i+1}/{len(key_chunks)} ---")
            
            # Extract answer candidates from chunk using NER and noun phrases
            answer_candidates = self.extract_key_phrases(chunk)
            
            if not answer_candidates:
                logging.warning(f"No answer candidates found in chunk {i+1}")
                continue
            
            # Generate questions using answer highlighting
            qa_pairs = self.generate_questions_with_highlights(
                chunk, answer_candidates, num_questions=3
            )
            
            for qa_pair in qa_pairs:
                if len(all_mcqs) >= max_mcqs:
                    break
                
                question = qa_pair['question']
                answer = qa_pair['answer']
                context = qa_pair['context']
                
                # Skip duplicate questions using semantic similarity
                question_embedding = self.semantic_model.encode(question, convert_to_tensor=True)
                
                is_duplicate = False
                if seen_question_embeddings:
                    similarities = util.cos_sim(question_embedding, torch.stack(seen_question_embeddings))
                    if torch.max(similarities) > 0.90:  # Slightly relaxed threshold
                        is_duplicate = True
                
                if is_duplicate:
                    logging.info(f"Skipping duplicate question: '{question[:50]}...'")
                    continue
                
                # Verify answer quality with enhanced QA model
                try:
                    qa_result = self.qa_pipeline(question=question, context=context)
                    predicted_answer = qa_result['answer'].strip()
                    confidence = qa_result['score']
                    
                    # Enhanced confidence threshold
                    if confidence < 0.35 or len(predicted_answer) < 1:
                        logging.warning(f"Skipping Q: '{question[:50]}...'. Low confidence ({confidence:.2f})")
                        continue
                    
                    logging.info(f"Generated Q: '{question[:50]}...' -> A: '{answer}' (Conf: {confidence:.2f})")
                    
                    # Generate distractors using multi-strategy approach
                    distractors = self.generate_semantic_distractors(
                        answer, context, cleaned_full_transcript, num_distractors=4
                    )
                    
                    # Validate distractors
                    valid_distractors = self.validate_distractors(question, answer, distractors)
                    
                    if len(valid_distractors) < min_distractors:
                        logging.warning(f"Insufficient valid distractors for: '{question[:50]}...'")
                        continue
                    
                    # Create options (limit to 4 total: 1 correct + 3 distractors)
                    final_distractors = valid_distractors[:3]
                    options = [answer] + final_distractors
                    random.shuffle(options)
                    
                    if len(options) < 2:
                        continue
                    
                    # Find correct option letter
                    correct_option_char = chr(65 + options.index(answer))
                    
                    # Create enhanced MCQ with additional metadata
                    mcq = {
                        'question': question,
                        'options': {chr(65 + i): opt for i, opt in enumerate(options)},
                        'correct_answer': correct_option_char,
                        'explanation': f"The correct answer is '{answer}' based on the context provided.",
                        'confidence': round(confidence, 3),
                        'difficulty': self.estimate_difficulty(question, answer, final_distractors),
                        'question_type': self.classify_question_type(question)
                    }
                    
                    all_mcqs.append(mcq)
                    seen_question_embeddings.append(question_embedding)
                    
                    logging.info(f"✅ Generated MCQ {len(all_mcqs)}: {question[:50]}...")
                    
                except Exception as e:
                    logging.error(f"Error processing question '{question[:50]}...': {e}")
                    continue
        
        logging.info(f"🎉 Finished processing. Generated {len(all_mcqs)} high-quality MCQs.")
        return all_mcqs

    def get_summary_stats(self, mcqs: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Get summary statistics of generated MCQs"""
        if not mcqs:
            return {}
        
        difficulties = [mcq.get('difficulty', 'Unknown') for mcq in mcqs]
        question_types = [mcq.get('question_type', 'Unknown') for mcq in mcqs]
        confidences = [mcq.get('confidence', 0) for mcq in mcqs]
        
        stats = {
            'total_mcqs': len(mcqs),
            'difficulty_distribution': {
                'Easy': difficulties.count('Easy'),
                'Medium': difficulties.count('Medium'), 
                'Hard': difficulties.count('Hard')
            },
            'question_type_distribution': {
                qtype: question_types.count(qtype) 
                for qtype in set(question_types)
            },
            'average_confidence': round(sum(confidences) / len(confidences), 3) if confidences else 0,
            'min_confidence': min(confidences) if confidences else 0,
            'max_confidence': max(confidences) if confidences else 0
        }
        
        return stats

    def export_mcqs(self, mcqs: List[Dict[str, Any]], filename: str = None) -> str:
        """Export MCQs to JSON file with metadata"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"enhanced_mcqs_{timestamp}.json"
        
        export_data = {
            'metadata': {
                'generated_at': datetime.now().isoformat(),
                'total_mcqs': len(mcqs),
                'generator_version': 'Enhanced_2.0',
                'improvements': [
                    'T5-base model for better question quality',
                    'RoBERTa-based QA for enhanced validation',
                    'Semantic chunking for better context',
                    'Multi-strategy distractor generation',
                    'Advanced preprocessing and cleaning'
                ]
            },
            'statistics': self.get_summary_stats(mcqs),
            'mcqs': mcqs
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, indent=2, ensure_ascii=False)
        
        logging.info(f"✅ MCQs exported to {filename}")
        return filename