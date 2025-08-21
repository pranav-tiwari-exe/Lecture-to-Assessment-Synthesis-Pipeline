# Enhanced test.py - Updated to work with the improved TranscriptQAGenerator

import time
import json
from datetime import datetime

# Import the enhanced TranscriptQAGenerator
from TranscriptQAGenerator import TranscriptQAGenerator

def print_separator(title=""):
    """Print a nice separator with optional title"""
    if title:
        print(f"\n{'='*60}")
        print(f" {title} ")
        print('='*60)
    else:
        print('-'*60)

def display_mcq(mcq, index):
    """Display a single MCQ in a nice format"""
    print(f"\n📝 MCQ #{index}")
    print(f"Question: {mcq['question']}")
    print("\nOptions:")
    
    for option_key, option_value in mcq['options'].items():
        # Add checkmark for correct answer
        marker = "✅" if option_key == mcq['correct_answer'] else "  "
        print(f"  {marker} {option_key}) {option_value}")
    
    print(f"\n💡 Explanation: {mcq['explanation']}")
    print(f"📊 Confidence: {mcq['confidence']}")
    print(f"🎯 Difficulty: {mcq['difficulty']}")
    print(f"🔍 Type: {mcq['question_type']}")
    print_separator()

def display_statistics(stats):
    """Display generation statistics"""
    print_separator("GENERATION STATISTICS")
    print(f"Total MCQs Generated: {stats['total_mcqs']}")
    print(f"Average Confidence: {stats['average_confidence']}")
    print(f"Confidence Range: {stats['min_confidence']} - {stats['max_confidence']}")
    
    print("\n📊 Difficulty Distribution:")
    for diff, count in stats['difficulty_distribution'].items():
        percentage = (count / stats['total_mcqs']) * 100 if stats['total_mcqs'] > 0 else 0
        print(f"  {diff}: {count} ({percentage:.1f}%)")
    
    print("\n🔍 Question Type Distribution:")
    for qtype, count in stats['question_type_distribution'].items():
        percentage = (count / stats['total_mcqs']) * 100 if stats['total_mcqs'] > 0 else 0
        print(f"  {qtype}: {count} ({percentage:.1f}%)")
    print_separator()

def run_enhanced_test():
    """
    Test the enhanced MCQ generator with improved features
    """
    print_separator("ENHANCED MCQ GENERATION TEST")
    print("🚀 Testing the Enhanced TranscriptQAGenerator")
    print("✨ New Features:")
    print("   - T5-base model for better question quality")
    print("   - RoBERTa-based QA for enhanced validation")
    print("   - Semantic chunking for better context")
    print("   - Multi-strategy distractor generation")
    print("   - Advanced preprocessing and cleaning")
    
    # 1. Initialize the enhanced generator
    print("\n🔄 Initializing Enhanced MCQ Generator...")
    start_time = time.time()
    
    try:
        qa_generator = TranscriptQAGenerator()
    except Exception as e:
        print(f"❌ Error during initialization: {e}")
        print("💡 Make sure you have installed all required dependencies:")
        print("   pip install torch transformers sentence-transformers spacy nltk")
        print("   python -m spacy download en_core_web_sm")
        return
    
    init_time = time.time() - start_time
    print(f"✅ Enhanced models loaded successfully in {init_time:.2f} seconds!")
    
    # 2. Enhanced sample transcript with more complex content
    sample_transcript = """
    Hello everyone, and welcome to today's training session. We'll be discussing the basics of machine learning, especially focusing on supervised learning techniques. Uh, so, as you're all aware, supervised learning involves labeled datasets, right? Where our goal is to map inputs to their corresponding outputs. Speaker 2:
Yeah, I think I got that part. Can you, uh, give an example? Like, what kind of datasets are we talking about? Speaker 1:
Absolutely. Think of a dataset of emails, where each is labeled as spam or not spam. Or, in image recognition, pictures of cats and dogs, labeled accordingly. These labels help the model learn patterns. Speaker 3:
But, um, what about unsupervised learning? How is that different? Is it, like, not involving labels? Speaker 1:
Exactly. Unsupervised learning deals with unlabeled data, aiming to find hidden patterns or groupings—clustering, for example. But today, we're focusing on supervised techniques. Speaker 2:
Got it. So, um, what's the typical pipeline for supervised learning? Speaker 1:
Good question. It generally involves data collection, preprocessing, feature engineering, model selection, training, evaluation, and deployment. Each step is crucial. Speaker 4:
Hey, quick note — when you say preprocessing, does that include, like, normalization and dealing with missing data? Speaker 1:
Yes, precisely. Normalization scales features; handling missing data involves imputation or removal. Ensuring data quality is fundamental. Speaker 3:
Okay, so I saw in the slides, they mentioned regression and classification. Can you clarify the difference? Speaker 1:
Sure. Regression predicts continuous outputs—like house prices—while classification predicts discrete categories, such as spam or not spam. Speaker 2:
Makes sense. And algorithms? Like, which algorithms are popular? Speaker 1:
Some common ones include Linear Regression, Logistic Regression, Decision Trees, Random Forests, Support Vector Machines, and Neural Networks. Speaker 4:
Neural networks? Like deep learning? Isn't that more complex? Speaker 1:
Yes, deep learning involves neural networks with many layers; they’re powerful but require more data and computational resources. Speaker 3:
Speaking of data, how much data is, um, enough for training these models? Speaker 1:
It depends on the problem complexity. Generally, more data helps. Small datasets may lead to overfitting; larger datasets improve generalization. Speaker 2:
Overfitting? That’s when the model learns the training data too well and fails on new data, right? Speaker 1:
Exactly. Techniques like cross-validation, regularization, and pruning help prevent overfitting. Speaker 4:
And what about the evaluation metrics? Which do we use? Speaker 1:
For classification, metrics include accuracy, precision, recall, F1-score, and ROC-AUC. For regression, mean squared error, mean absolute error, etc. Speaker 3:
Okay, that’s a lot to take in. Is there, like, a recommended starting point for beginners? Speaker 1:
Definitely. Start with simple algorithms like Linear Regression or Logistic Regression, and practice on datasets like Iris or Titanic. Speaker 2:
Thanks. One last thing — how do I know if my model is good enough? Speaker 1:
Use validation techniques and evaluation metrics. Also, check if the model performs well on unseen test data rather than just training data. Speaker 4:
Perfect. Thanks for the clarity. I guess I need to review the slides and maybe, uh, practice with some datasets. Speaker 1:
Great. Practice and experimentation are key. Feel free to ask questions anytime, and I’ll be here to help.
End of Transcript
This transcript covers diverse topics, speakers, informal speech, technical language, and noise elements, making it ideal for testing your MCQ generator. Let me know if you'd like this in a specific format or with additional content!
    """
    
    # 3. Generate MCQs with enhanced settings
    print("\n🎯 Generating MCQs from enhanced transcript...")
    print(f"📄 Transcript length: {len(sample_transcript)} characters")
    
    start_time = time.time()
    
    try:
        # Test with different parameters
        mcqs = qa_generator.generate_qa_pairs(
            transcript=sample_transcript, 
            max_mcqs=8,              # Generate up to 8 MCQs
            min_distractors=2        # Require at least 2 distractors
        )
    except Exception as e:
        print(f"❌ Error during MCQ generation: {e}")
        return
    
    gen_time = time.time() - start_time
    print(f"✅ Enhanced generation complete in {gen_time:.2f} seconds!")
    
    # 4. Display results with enhanced formatting
    if mcqs:
        print(f"\n🎉 Successfully generated {len(mcqs)} high-quality MCQs!")
        
        # Display each MCQ
        for i, mcq in enumerate(mcqs, 1):
            display_mcq(mcq, i)
        
        # 5. Display enhanced statistics
        stats = qa_generator.get_summary_stats(mcqs)
        display_statistics(stats)
        
        # 6. Export results with metadata
        print("\n💾 Exporting results...")
        try:
            filename = qa_generator.export_mcqs(mcqs)
            print(f"✅ MCQs exported to: {filename}")
            print("📁 The exported file includes:")
            print("   - All generated MCQs")
            print("   - Generation statistics") 
            print("   - Metadata about improvements")
            print("   - Timestamp and version info")
        except Exception as e:
            print(f"⚠️ Error exporting MCQs: {e}")
        
        # 7. Performance summary
        print_separator("PERFORMANCE SUMMARY")
        print(f"⏱️  Total Time: {init_time + gen_time:.2f} seconds")
        print(f"🏗️  Initialization: {init_time:.2f}s")
        print(f"⚡ Generation: {gen_time:.2f}s")
        print(f"📈 MCQs per second: {len(mcqs)/gen_time:.2f}")
        print(f"🎯 Success Rate: {len(mcqs)}/8 requested")
        
        # 8. Quality indicators
        avg_confidence = stats['average_confidence']
        if avg_confidence >= 0.7:
            quality_rating = "Excellent 🌟"
        elif avg_confidence >= 0.5:
            quality_rating = "Good ✅"
        elif avg_confidence >= 0.4:
            quality_rating = "Fair ⚠️"
        else:
            quality_rating = "Needs Improvement 🔧"
            
        print(f"🏆 Quality Rating: {quality_rating}")
        print(f"📊 Average Confidence: {avg_confidence}")
        
    else:
        print("❌ No MCQs were generated.")
        print("💡 This could be due to:")
        print("   - Transcript too short or lacks factual content")
        print("   - Strict quality filtering removing low-quality questions")
        print("   - Model initialization issues")
        print("   - Try with a longer, more detailed transcript")
    
    print_separator("TEST COMPLETE")
    print("🎯 Enhanced MCQ Generator Test Finished!")
    print("📚 For more information, check the generated JSON export file")

def run_comparison_test():
    """
    Quick test to demonstrate improvements over basic approach
    """
    print_separator("QUICK COMPARISON TEST")
    
    # Short test transcript
    short_transcript = """
    Python is a high-level programming language created by Guido van Rossum in 1991. 
    It emphasizes code readability and simplicity. Python supports multiple programming 
    paradigms including procedural, object-oriented, and functional programming.
    """
    
    print("🔍 Testing with shorter transcript...")
    
    try:
        qa_generator = TranscriptQAGenerator()
        mcqs = qa_generator.generate_qa_pairs(short_transcript, max_mcqs=3)
        
        if mcqs:
            print(f"✅ Generated {len(mcqs)} MCQs from short transcript!")
            for i, mcq in enumerate(mcqs, 1):
                print(f"\n{i}. {mcq['question']}")
                correct_key = mcq['correct_answer']
                print(f"   Answer: {mcq['options'][correct_key]} (Confidence: {mcq['confidence']})")
        else:
            print("❌ No MCQs generated from short transcript")
            
    except Exception as e:
        print(f"❌ Comparison test failed: {e}")

def main():
    """Main test function"""
    print("🚀 Enhanced MCQ Generator Test Suite")
    print("Choose test type:")
    print("1. Full Enhanced Test (recommended)")
    print("2. Quick Comparison Test")
    print("3. Both tests")
    
    choice = input("\nEnter choice (1-3) or press Enter for full test: ").strip()
    
    if choice == "2":
        run_comparison_test()
    elif choice == "3":
        run_enhanced_test()
        run_comparison_test()
    else:  # Default to full test
        run_enhanced_test()

if __name__ == "__main__":
    main()