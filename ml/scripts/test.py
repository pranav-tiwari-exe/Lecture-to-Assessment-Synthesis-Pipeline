# test.py
import time
# Ensure your class is saved in a file named 'generator.py' in the same directory
from TranscriptQAGenerator import TranscriptQAGenerator

def run_test():
    """
    Initializes the QA generator, processes a sample transcript,
    and prints the generated question-answer pairs.
    """
    print("--- Starting QA Generation Test ---")

    # 1. Initialize the generator
    # This step loads all the necessary models into memory.
    print("Initializing the QA Generator (this may take a moment)...")
    start_time = time.time()
    try:
        qa_generator = TranscriptQAGenerator()
    except Exception as e:
        print(f"Error during initialization: {e}")
        return
        
    init_time = time.time() - start_time
    print(f"✅ Initialization complete in {init_time:.2f} seconds.")

    # 2. Provide a sample transcript for testing
    sample_transcript = """Got it 👍. I’ll create a **long, detailed transcript** of a panel-style discussion on **AI and IT development**, where multiple speakers share their views. This will read like a natural conversation and cover a wide range of content so it feels rich, engaging, and useful.

---

# 📌 Transcript: AI and IT Development – The Future of Technology

**Host (Moderator):**
Welcome everyone to today’s panel discussion on *“AI and IT Development: Shaping the Future of Technology.”* We’ve gathered industry experts to talk about how artificial intelligence is transforming IT, from automation and cloud computing to cybersecurity and software engineering practices. Let’s dive right in.

---

**Speaker 1 (AI Researcher):**
AI is no longer just a research subject—it’s becoming the backbone of IT infrastructure. In the past, IT was about servers, storage, and networks. Now, we’re seeing machine learning models integrated directly into these systems. For example, data centers are managed with predictive analytics to reduce downtime. Algorithms forecast hardware failures before they happen. This wasn’t possible five years ago at scale.

---

**Speaker 2 (Software Engineer):**
Exactly. From a software development perspective, AI is rewriting the rules of coding itself. Developers now rely on AI-assisted coding tools like GitHub Copilot. These tools not only suggest snippets but also generate entire functions based on natural language descriptions. This changes the workflow of IT development teams—less time debugging boilerplate code, more focus on designing architecture and solving real problems.

---

**Speaker 3 (IT Security Specialist):**
I’d add that security is where AI’s role is both promising and challenging. On one hand, AI-based intrusion detection systems spot anomalies that traditional rule-based systems miss. On the other hand, attackers also use AI for phishing campaigns, malware obfuscation, and deepfake-based social engineering. IT teams need to constantly adapt. Cybersecurity in the age of AI is not just about defense—it’s about anticipating offensive AI too.

---

**Speaker 4 (Cloud & DevOps Expert):**
Let’s not forget DevOps and cloud computing. Automation pipelines are now powered by AI, meaning deployment strategies can adjust dynamically based on usage data. Imagine Kubernetes clusters that don’t just scale automatically but optimize themselves intelligently—shifting workloads based on predicted demand. This reduces costs and improves resilience.

---

**Moderator:**
That’s fascinating. What about the workforce impact? How do IT professionals fit in with AI doing so much of the work?

---

**Speaker 2 (Software Engineer):**
Great question. The fear of AI “replacing jobs” is common, but what we’re actually seeing is *role transformation.* Routine tasks—like writing repetitive code, generating test cases, or monitoring logs—are increasingly automated. But this creates demand for new skills: prompt engineering, AI model fine-tuning, data pipeline management. IT professionals will still be needed, but their roles will evolve from manual execution to supervision and innovation.

---

**Speaker 1 (AI Researcher):**
Exactly. Think of it this way—AI is becoming a co-pilot, not a pilot. It augments human capabilities. Just as spreadsheets didn’t eliminate accountants but made them more effective, AI won’t remove IT jobs entirely. It’ll elevate them.

---

**Speaker 3 (IT Security Specialist):**
I’d like to stress that with this evolution, ethical considerations matter. IT development is moving into areas where bias, fairness, and transparency are crucial. For example, if an AI-based IT monitoring system wrongly flags certain user behaviors, it can cause massive business disruptions. Responsible AI integration is just as important as technical advancement.

---

**Speaker 4 (Cloud & DevOps Expert):**
And sustainability too. AI systems consume massive computational resources. IT infrastructure needs to become greener—leveraging renewable-powered data centers, efficient cooling, and algorithmic optimization. The future isn’t just about faster AI but smarter AI that uses fewer resources.

---

**Moderator:**
Let’s touch on innovation. What new frontiers in IT development will AI unlock in the next decade?

---

**Speaker 1 (AI Researcher):**
We’ll see *autonomous IT systems.* Imagine networks that configure themselves, cloud infrastructures that heal themselves, and applications that evolve based on user feedback in real time. This is moving toward what we call “self-driving IT.”

---

**Speaker 2 (Software Engineer):**
I also think we’ll witness hyper-personalized software. Instead of one-size-fits-all apps, AI will enable apps that morph based on the user’s behavior. The IT development cycle will shift from “build once, deploy to all” to “build frameworks that adapt per individual.”

---

**Speaker 3 (IT Security Specialist):**
On the security side, quantum computing combined with AI could radically change encryption. IT teams must prepare for a post-quantum world where traditional algorithms are obsolete. AI may also help design new cryptographic methods resistant to quantum attacks.

---

**Speaker 4 (Cloud & DevOps Expert):**
And don’t forget edge computing. With AI models running on devices, IT won’t just be cloud-centric. Smart cities, autonomous vehicles, and IoT devices will require decentralized intelligence. IT development will need to support distributed AI across billions of endpoints.

---

**Moderator:**
That’s powerful. To wrap up, let me ask each of you in one sentence: What advice would you give to IT professionals preparing for an AI-driven future?

---

* **Speaker 1 (AI Researcher):** Stay curious—learn how AI models work under the hood, not just how to use them.
* **Speaker 2 (Software Engineer):** Embrace AI tools, but focus on problem-solving and creativity, because that’s where humans shine.
* **Speaker 3 (IT Security Specialist):** Think like both a defender and an attacker—AI makes the battlefield more dynamic.
* **Speaker 4 (Cloud & DevOps Expert):** Build skills in automation, cloud, and data—these are the foundations where AI thrives.

---

**Moderator:**
Thank you to all our speakers. This has been an enlightening conversation about the intersection of AI and IT development. Clearly, the future belongs to those who adapt, innovate, and collaborate with AI rather than fear it.

---

👉 This transcript gives you **lots of content**—touching on research, development, DevOps, security, workforce transformation, ethics, sustainability, and future trends.

Would you like me to also **make this into a structured article/essay** (instead of a dialogue) so it can be used as a report, blog, or study material?

    """

    # 3. Generate QA pairs from the transcript
    print("\nGenerating Question-Answer pairs...")
    start_time = time.time()
    # We will request 5 high-quality, unique QA pairs.
    qa_pairs = qa_generator.generate_qa_pairs(transcript=sample_transcript, max_mcqs=50)
    gen_time = time.time() - start_time
    print(f"✅ Generation complete in {gen_time:.2f} seconds.")

    # 4. Print the formatted results
    print(f"\n--- Generated {len(qa_pairs)} Unique QA Pairs ---")
    
    if qa_pairs:
        for i, pair in enumerate(qa_pairs, 1):
            print("\n" + "="*50)
            print(f"QA Pair #{i}")
            print(f"  Question: {pair['question']}")
            print(f"  Answer: {pair['answer']}")
            print(f"  Confidence: {pair['confidence']}")
            # The context shows the source text chunk used for generation
            print(f"  Context: \"{pair['context'][:200]}...\"")
        print("="*50)
    else:
        print("\nNo high-quality QA pairs were generated. This could be due to a short transcript or strict filtering.")

    print("\n--- Test Complete ---")


if __name__ == "__main__":
    run_test()