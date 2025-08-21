# generator.py
import torch
from transformers import T5ForConditionalGeneration, T5Tokenizer, pipeline
from typing import List, Dict, Any
import re
import nltk
from sentence_transformers import SentenceTransformer, util
import random
import spacy
import logging

# Configure logging to see the generation process and diagnose issues
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class TranscriptQAGenerator:
    """
    An advanced ML Model for generating high-quality, semantically unique, and fact-checked
    MCQ Question-Answer pairs from input transcripts.
    This version is revised for improved robustness and output.
    """
    
    def __init__(self, model_name: str = "valhalla/t5-small-qa-qg-hl"):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        print(f"Using device: {self.device}")
        
        # --- Model for Question Generation ---
        self.qg_tokenizer = T5Tokenizer.from_pretrained(model_name)
        self.qg_model = T5ForConditionalGeneration.from_pretrained(model_name).to(self.device)
        
        # --- Model for Answering Generated Questions ---
        self.qa_pipeline = pipeline(
            "question-answering", 
            model="distilbert-base-cased-distilled-squad",
            device=0 if torch.cuda.is_available() else -1
        )
        
        # --- Model for Semantic Similarity ---
        self.semantic_model = SentenceTransformer('all-MiniLM-L6-v2', device=self.device)
        
        # --- Model for Named Entity Recognition (for distractor generation) ---
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
            nltk.download('punkt')
        
        self.is_loaded = True
        print("Advanced models initialized successfully!")
    
    def preprocess_transcript(self, transcript: str, chunk_size: int = 5, overlap: int = 2) -> List[str]:
        transcript = re.sub(r'\s+', ' ', transcript.strip())
        sentences = nltk.sent_tokenize(transcript)
        chunks = []
        for i in range(0, len(sentences), chunk_size - overlap):
            chunk = ' '.join(sentences[i:i + chunk_size])
            # Ensure chunk is not too short
            if len(chunk.split()) > 25:
                chunks.append(chunk)
        return chunks

    def extract_key_information(self, chunks: List[str], top_k: int = 15) -> List[str]:
        if not chunks: return []
        if len(chunks) <= top_k: return chunks
        
        embeddings = self.semantic_model.encode(chunks, convert_to_tensor=True)
        cosine_scores = util.cos_sim(embeddings, embeddings)
        centrality_scores = cosine_scores.mean(axis=1)
        # Select top k most central chunks
        top_indices = torch.topk(centrality_scores, k=min(top_k, len(chunks))).indices
        
        return [chunks[i] for i in sorted(top_indices.tolist())]

    def generate_questions(self, context: str, num_questions: int = 3) -> List[str]:
        input_text = f"generate questions: {context}"
        input_ids = self.qg_tokenizer.encode(input_text, return_tensors="pt", max_length=512, truncation=True).to(self.device)
        
        outputs = self.qg_model.generate(
            input_ids,
            max_length=128,
            num_beams=5,
            num_return_sequences=num_questions,
            early_stopping=True,
            no_repeat_ngram_size=2,
            temperature=1.2, # Add some creativity
            do_sample=True
        )
        
        questions = [self.qg_tokenizer.decode(out, skip_special_tokens=True) for out in outputs]
        valid_questions = []
        for q in questions:
            # Clean up generated questions
            q = re.sub(r'generate questions?:', '', q, flags=re.IGNORECASE).strip()
            # Filter for well-formed questions
            if q and len(q.split()) > 4 and q.endswith('?'):
                valid_questions.append(q)
        return list(set(valid_questions))

    def extract_entities_with_ner(self, text: str) -> Dict[str, List[str]]:
        doc = self.ner_model(text)
        entities = {}
        for ent in doc.ents:
            if ent.label_ not in entities: entities[ent.label_] = []
            if ent.text.strip(): entities[ent.label_].append(ent.text.strip())
            
        for label in entities:
            # Sort by length to prioritize more specific entities
            entities[label] = sorted(list(set(entities[label])), key=len, reverse=True)
        return entities

    def generate_semantic_distractors(self, correct_answer: str, context: str, num_distractors: int = 3) -> List[str]:
        all_entities_by_type = self.extract_entities_with_ner(context)
        answer_doc = self.ner_model(correct_answer)
        answer_type = answer_doc.ents[0].label_ if answer_doc.ents else None

        candidate_pool = []
        if answer_type:
            candidate_pool.extend(all_entities_by_type.get(answer_type, []))
            
        for label, entities in all_entities_by_type.items():
            if label != answer_type: candidate_pool.extend(entities)
            
        candidate_pool = [cand for cand in list(set(candidate_pool)) if cand.lower() != correct_answer.lower() and len(cand) > 1]
        
        if not candidate_pool: return []
        
        if len(candidate_pool) <= num_distractors:
            random.shuffle(candidate_pool)
            return candidate_pool
        
        answer_embedding = self.semantic_model.encode(correct_answer, convert_to_tensor=True)
        candidate_embeddings = self.semantic_model.encode(candidate_pool, convert_to_tensor=True)
        
        similarities = util.cos_sim(answer_embedding, candidate_embeddings)[0]
        top_indices = torch.topk(similarities, k=min(num_distractors * 2, len(similarities))).indices
        
        distractors = []
        for i in top_indices:
            distractor = candidate_pool[i.item()]
            if distractor.lower() != correct_answer.lower() and distractor not in distractors:
                distractors.append(distractor)

        return distractors[:num_distractors]

    def generate_qa_pairs(self, transcript: str, max_mcqs: int = 10) -> List[Dict[str, Any]]:
        if not self.is_loaded:
            raise RuntimeError("Models are not properly loaded.")
        
        chunks = self.preprocess_transcript(transcript)
        if not chunks:
            logging.warning("Preprocessing returned no chunks from the transcript.")
            return []
        
        key_chunks = self.extract_key_information(chunks, top_k=15)
        
        all_mcqs = []
        seen_question_embeddings = []

        for i, chunk in enumerate(key_chunks):
            if len(all_mcqs) >= max_mcqs: break
            
            logging.info(f"--- Processing Chunk {i+1}/{len(key_chunks)} ---")
            
            # Generate questions from the original, detailed chunk
            questions = self.generate_questions(chunk, num_questions=2)
            if not questions:
                logging.warning(f"No valid questions generated for chunk: '{chunk[:80]}...'")
                continue
            
            for question in questions:
                question_embedding = self.semantic_model.encode(question, convert_to_tensor=True)
                
                is_duplicate = False
                if seen_question_embeddings:
                    similarities = util.cos_sim(question_embedding, torch.stack(seen_question_embeddings))
                    if torch.max(similarities) > 0.95: is_duplicate = True
                
                if is_duplicate:
                    logging.info(f"Skipping duplicate question: '{question}'")
                    continue

                try:
                    # Get answer from the original, detailed chunk
                    qa_result = self.qa_pipeline(question=question, context=chunk)
                    correct_answer = qa_result['answer'].strip()
                    confidence = qa_result['score']
                    
                    # Relaxed confidence threshold + Logging
                    if confidence < 0.40 or len(correct_answer) < 1:
                        logging.warning(f"Skipping Q: '{question}'. Low confidence ({confidence:.2f}) or no answer.")
                        continue
                    
                    logging.info(f"Generated Q: '{question}' -> A: '{correct_answer}' (Conf: {confidence:.2f})")

                    distractors = self.generate_semantic_distractors(correct_answer, chunk, num_distractors=3)
                    
                    # Accept fewer than 3 distractors
                    if len(distractors) < 1:
                        logging.warning(f"Could not generate enough distractors for answer '{correct_answer}'. Skipping.")
                        continue
                    
                    options = sorted(list(set([correct_answer] + distractors)), key=lambda x: random.random())
                    
                    if len(options) < 2: continue

                    correct_option_char = chr(65 + options.index(correct_answer))

                    all_mcqs.append({
                        'question': question,
                        'options': {chr(65 + i): opt for i, opt in enumerate(options)},
                        'correct_answer': correct_option_char,
                        'explanation': f"The correct answer is '{correct_answer}'.",
                        'confidence': round(confidence, 2)
                    })
                    seen_question_embeddings.append(question_embedding)

                    if len(all_mcqs) >= max_mcqs: break
                
                except Exception as e:
                    logging.error(f"An error occurred while processing question '{question}': {e}")
                    continue
                
        logging.info(f"--- Finished processing. Generated {len(all_mcqs)} MCQs. ---")
        return all_mcqs

