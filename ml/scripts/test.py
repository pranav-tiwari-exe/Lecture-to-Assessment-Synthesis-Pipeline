# test.py
import time
# The generator class must be in a file named 'generator.py' in the same folder.
# The class name within that file is TranscriptQAGenerator.
from TranscriptQAGenerator import TranscriptQAGenerator

def run_test():
    """
    Initializes the QA generator, processes a sample transcript,
    and prints the generated multiple-choice questions.
    """
    print("--- Starting MCQ Generation Test ---")

    # 1. Initialize the generator
    print("Initializing the MCQ Generator (this may take a moment)...")
    start_time = time.time()
    try:
        qa_generator = TranscriptQAGenerator()
    except Exception as e:
        print(f"Error during initialization: {e}")
        return
        
    init_time = time.time() - start_time
    print(f"✅ Initialization complete in {init_time:.2f} seconds.")

    # 2. Provide a sample transcript for testing
    sample_transcript = """
    Artificial intelligence (AI) is a wide-ranging branch of computer science concerned with building smart machines capable of performing tasks that typically require human intelligence. 
    The term was coined in 1956 by John McCarthy at the Dartmouth Conference. AI has several sub-fields, including machine learning (ML), which focuses on the idea that machines should be able to learn and adapt through experience. 
    Deep learning is a subset of machine learning based on artificial neural networks. The Turing Test, developed by Alan Turing in 1950, is a test of a machine's ability to exhibit intelligent behavior equivalent to, or indistinguishable from, that of a human. 
    Modern AI systems are often used for natural language processing, image recognition, and expert systems. For instance, Google's AlphaGo is a famous example of AI that defeated a world champion Go player, Lee Sedol, in 2016.
    """

    # 3. Generate MCQs from the transcript
    print("\nGenerating Multiple-Choice Questions...")
    start_time = time.time()
    qa_pairs = qa_generator.generate_qa_pairs(transcript=sample_transcript, max_mcqs=5)
    gen_time = time.time() - start_time
    print(f"✅ Generation complete in {gen_time:.2f} seconds.")

    # 4. Print the formatted results
    print(f"\n--- Generated {len(qa_pairs)} Unique MCQs ---")
    
    if qa_pairs:
        for i, pair in enumerate(qa_pairs, 1):
            print("\n" + "="*50)
            print(f"MCQ #{i}")
            print(f"  Question: {pair['question']}")
            # --- CORRECTED BLOCK START ---
            print("  Options:")
            for option, text in pair['options'].items():
                print(f"    {option}) {text}")
            print(f"  Correct Answer: {pair['correct_answer']}")
            print(f"  Explanation: {pair['explanation']}")
            print(f"  Confidence: {pair['confidence']}")
            # --- CORRECTED BLOCK END ---
        print("="*50)
    else:
        print("\nNo high-quality MCQs were generated. This could be due to a short transcript or strict filtering.")

    print("\n--- Test Complete ---")


if __name__ == "__main__":
    run_test()