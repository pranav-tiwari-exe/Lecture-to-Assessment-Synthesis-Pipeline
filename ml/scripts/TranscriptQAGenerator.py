# generator.py
import torch
from transformers import T5ForConditionalGeneration, T5Tokenizer, pipeline
from typing import List, Dict, Any
import re
import nltk
from sentence_transformers import SentenceTransformer, util
import random
import spacy

class TranscriptQAGenerator:
    """
    An advanced ML Model for generating high-quality, semantically unique, and fact-checked
    MCQ Question-Answer pairs from input transcripts.
    """
    
    def __init__(self, model_name: str = "valhalla/t5-small-qa-qg-hl"):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        print(f"Using device: {self.device}")
        
        self.qg_tokenizer = T5Tokenizer.from_pretrained(model_name)
        self.qg_model = T5ForConditionalGeneration.from_pretrained(model_name).to(self.device)
        
        self.qa_pipeline = pipeline(
            "question-answering", 
            model="distilbert-base-cased-distilled-squad",
            device=0 if torch.cuda.is_available() else -1
        )
        
        self.summarizer = pipeline(
            "summarization",
            model="t5-small",
            device=0 if torch.cuda.is_available() else -1
        )

        self.semantic_model = SentenceTransformer('all-MiniLM-L6-v2')
        
        try:
            self.ner_model = spacy.load("en_core_web_sm")
        except OSError:
            print("Downloading 'en_core_web_sm' for spaCy...")
            from spacy.cli import download
            download("en_core_web_sm")
            self.ner_model = spacy.load("en_core_web_sm")

        try:
            nltk.data.find('tokenizers/punkt')
        except LookupError:
            nltk.download('punkt')
        
        self.is_loaded = True
        print("Advanced models initialized successfully!")
    
    def preprocess_transcript(self, transcript: str, chunk_size: int = 4, overlap: int = 1) -> List[str]:
        transcript = re.sub(r'\s+', ' ', transcript.strip())
        sentences = nltk.sent_tokenize(transcript)
        chunks = []
        for i in range(0, len(sentences), chunk_size - overlap):
            chunk = ' '.join(sentences[i:i + chunk_size])
            if len(chunk.split()) > 25:
                chunks.append(chunk)
        return chunks

    def extract_key_information(self, chunks: List[str], top_k: int = 10) -> List[str]:
        if not chunks: return []
        if len(chunks) <= top_k: return chunks
        
        embeddings = self.semantic_model.encode(chunks, convert_to_tensor=True)
        cosine_scores = util.cos_sim(embeddings, embeddings)
        centrality_scores = cosine_scores.mean(axis=1)
        top_indices = torch.topk(centrality_scores, k=min(top_k, len(chunks))).indices
        
        return [chunks[i] for i in sorted(top_indices.tolist())]

    def generate_questions(self, context: str, num_questions: int = 3) -> List[str]:
        input_text = f"generate questions: {context}"
        input_ids = self.qg_tokenizer.encode(input_text, return_tensors="pt").to(self.device)
        
        outputs = self.qg_model.generate(
            input_ids, max_length=128, num_beams=5, num_return_sequences=num_questions,
            early_stopping=True, no_repeat_ngram_size=2, temperature=1.2, do_sample=True
        )
        
        questions = [self.qg_tokenizer.decode(out, skip_special_tokens=True) for out in outputs]
        valid_questions = []
        for q in questions:
            q = re.sub(r'generate questions?:', '', q, flags=re.IGNORECASE).strip()
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
        
        answer_embedding = self.semantic_model.encode(correct_answer, convert_to_tensor=True)
        candidate_embeddings = self.semantic_model.encode(candidate_pool, convert_to_tensor=True)
        
        similarities = util.cos_sim(answer_embedding, candidate_embeddings)[0]
        top_indices = torch.topk(similarities, k=min(num_distractors * 2, len(similarities))).indices
        distractors = [candidate_pool[i] for i in top_indices if candidate_pool[i].lower() != correct_answer.lower()]
        
        return distractors[:num_distractors]

    def generate_qa_pairs(self, transcript: str, max_mcqs: int = 10) -> List[Dict[str, Any]]:
        if not self.is_loaded:
            raise RuntimeError("Models are not properly loaded.")
            
        chunks = self.preprocess_transcript(transcript)
        if not chunks: return []
            
        key_chunks = self.extract_key_information(chunks, top_k=15)
        
        all_mcqs = []
        seen_question_embeddings = []

        for chunk in key_chunks:
            if len(all_mcqs) >= max_mcqs: break
            
            try:
                input_token_length = len(self.summarizer.tokenizer.encode(chunk))
                summary_max_length = max(25, int(input_token_length * 0.7))
                summary_min_length = max(10, int(input_token_length * 0.2))

                summary_result = self.summarizer(
                    chunk, max_length=summary_max_length, min_length=summary_min_length, 
                    max_new_tokens=None, do_sample=False
                )
                fact_context = summary_result[0]['summary_text']

                if len(fact_context.split()) < 8: continue
            except Exception:
                continue

            questions = self.generate_questions(fact_context, num_questions=2)
            
            for question in questions:
                question_embedding = self.semantic_model.encode(question, convert_to_tensor=True)
                
                is_duplicate = False
                if len(seen_question_embeddings) > 0:
                    similarities = util.cos_sim(question_embedding, torch.stack(seen_question_embeddings))
                    if torch.max(similarities) > 0.95:
                        is_duplicate = True
                if is_duplicate: continue

                context_embedding = self.semantic_model.encode(fact_context, convert_to_tensor=True)
                # --- TUNED FILTER 1: Relaxed relevance score ---
                relevance_score = util.cos_sim(question_embedding, context_embedding)[0][0].item()
                if relevance_score < 0.55: continue

                try:
                    qa_result = self.qa_pipeline(question=question, context=fact_context)
                    correct_answer = qa_result['answer'].strip()
                    confidence = qa_result['score']
                    
                    # --- TUNED FILTER 2: Relaxed confidence threshold ---
                    if confidence < 0.75 or len(correct_answer) < 1: continue

                    distractors = self.generate_semantic_distractors(correct_answer, fact_context, num_distractors=3)
                    if len(distractors) < 3: continue
                    
                    options = [correct_answer] + distractors
                    random.shuffle(options)
                    correct_option_char = chr(65 + options.index(correct_answer))

                    all_mcqs.append({
                        'question': question,
                        'options': {chr(65 + i): opt for i, opt in enumerate(options)},
                        'correct_answer': correct_option_char,
                        'explanation': f"The correct answer is '{correct_answer}' as stated in the summarized context.",
                        'confidence': round(confidence, 2)
                    })
                    seen_question_embeddings.append(question_embedding)

                    if len(all_mcqs) >= max_mcqs: break
                except Exception:
                    continue
            
        return all_mcqs