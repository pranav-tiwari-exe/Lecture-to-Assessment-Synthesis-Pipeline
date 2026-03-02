package com.ltm.backend.services;

import com.ltm.backend.Data.MCQ_response;
import tools.jackson.databind.JsonNode;
import tools.jackson.databind.ObjectMapper;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import org.springframework.web.reactive.function.client.WebClient;
import reactor.core.publisher.Flux;
import reactor.core.publisher.Mono;

import java.time.Duration;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Map;

@Service("llm1Service")
public class LLM1Service {
    @Value("${llm1Key}")
    private String llm1Key;
    @Value("${llm1Uri}")
    private String llm1Uri;

    private final WebClient webClient;
    private final ObjectMapper objectMapper;

    public LLM1Service(WebClient webClient, ObjectMapper objectMapper) {
        this.webClient = webClient;
        this.objectMapper = objectMapper;
    }

    public Mono<MCQ_response> generate(String fullTranscript) {
        // Chunk transcript to max 400 words using sliding window to handle unpunctuated text (like YouTube)
        List<String> chunks = chunkTranscript(fullTranscript, 400);

        return Flux.fromIterable(chunks)
                .flatMap(this::generateSingleChunk, 3) // Concurrency limit of 3
                .reduce(new MCQ_response(new ArrayList<>(), "Google Gemini"), (mergedResult, nextChunk) -> {
                    if (nextChunk != null && nextChunk.getResponse() != null) {
                        mergedResult.getResponse().addAll(nextChunk.getResponse());
                    }
                    return mergedResult;
                })
                .defaultIfEmpty(new MCQ_response(new ArrayList<>(), "Google Gemini"));
    }

    private Mono<MCQ_response> generateSingleChunk(String chunk) {
        String prompt = "You are an expert quiz creator. Your task is to perform an EXHAUSTIVE extraction of the provided transcript chunk. " +
                "Generate the ABSOLUTE MAXIMUM number of unique, non-repeating multiple-choice questions possible. " +
                "Follow these strict rules:\n" +
                "1. Go sentence-by-sentence. Extract every single fact, detail, and concept.\n" +
                "2. Ensure no two questions test the exact same concept (no duplicates).\n" +
                "3. Set the 'provider' field exactly to 'Google Gemini'.\n\n" +
                "Transcript Chunk: " + chunk;

        Map<String, Object> MCQSchema = Map.of(
                "type", "OBJECT",
                "properties", Map.of(
                        "question", Map.of("type", "STRING", "description", "A tricky multiple choice question about the topic."),
                        "options", Map.of("type", "ARRAY", "items", Map.of("type", "STRING"), "description", "Exactly 4 options. Only one can be correct."),
                        "correctAnswer", Map.of("type", "STRING", "description", "Must exactly match one of the strings in the options array.")
                ),
                "required", List.of("question", "options", "correctAnswer")
        );

        Map<String, Object> responseBody = Map.of(
                "type", "OBJECT",
                "properties", Map.of(
                        "response", Map.of("type", "ARRAY", "items", MCQSchema),
                        "provider", Map.of("type", "STRING")
                ),
                "required", List.of("response", "provider")
        );

        Map<String, Object> requestBody = Map.of(
                "contents", List.of(Map.of("parts", List.of(Map.of("text", prompt)))),
                "generationConfig", Map.of("responseMimeType", "application/json", "responseSchema", responseBody)
        );

        return webClient.post()
                .uri(llm1Uri + "?key=" + llm1Key)
                .bodyValue(requestBody)
                .retrieve()
                .bodyToMono(JsonNode.class)
                .timeout(Duration.ofSeconds(45))
                .map(jsonResponse -> {
                    try {
                        String jsonString = jsonResponse.path("candidates").get(0).path("content").path("parts").get(0).path("text").asText();
                        return objectMapper.readValue(jsonString, MCQ_response.class);
                    } catch (Exception e) {
                        throw new RuntimeException("Failed to parse llm1 response: " + e.getMessage(), e);
                    }
                })
                .onErrorResume(e -> Mono.just(new MCQ_response(new ArrayList<>(), "Gemini (Failed Chunk)")));
    }

    public Mono<List<Double>> validate(String transcript, MCQ_response response) {
        String promptTemplate = "### TASK\n" +
                "Analyze the provided transcript and the list of generated MCQs. Score each question on a scale of 1-10 based on its RELEVANCY to the transcript. Detect duplicate questions.\n\n" +
                "### RULES\n" +
                "1. SCORE: 10 = crucial info, 1 = hallucinated.\n" +
                "2. DEDUPLICATION: If a question is a duplicate of one earlier in the list, assign it -1.\n" +
                "3. OUTPUT: Return an array of numbers representing scores in the exact order as input.\n\n" +
                "TRANSCRIPT: %s\n\nGENERATED MCQs: %s";

        String prompt = String.format(promptTemplate, transcript, response.toString());

        Map<String, Object> scoreSchema = Map.of(
                "type", "ARRAY",
                "items", Map.of("type", "NUMBER", "description", "Score from 1.0 to 10.0, or -1.0 for duplicates")
        );

        Map<String, Object> requestBody = Map.of(
                "contents", List.of(Map.of("parts", List.of(Map.of("text", prompt)))),
                "generationConfig", Map.of("responseMimeType", "application/json", "responseSchema", scoreSchema)
        );

        return webClient.post()
                .uri(llm1Uri + "?key=" + llm1Key)
                .bodyValue(requestBody)
                .retrieve()
                .bodyToMono(JsonNode.class)
                .timeout(Duration.ofSeconds(45))
                .map(jsonResponse -> {
                    try {
                        String jsonString = jsonResponse.path("candidates").get(0).path("content").path("parts").get(0).path("text").asText();
                        Double[] scoresArray = objectMapper.readValue(jsonString, Double[].class);
                        return Arrays.asList(scoresArray);
                    } catch (Exception e) {
                        throw new RuntimeException("Failed to parse llm1 validation: " + e.getMessage(), e);
                    }
                })
                .onErrorResume(e -> fillFallbackScores(response.getResponse().size()));
    }

    // --- UTILITIES ---

    private List<String> chunkTranscript(String transcript, int maxWordsPerChunk) {
        // 1. Split by whitespace since we can't trust punctuation
        String[] words = transcript.split("\\s+");
        List<String> chunks = new ArrayList<>();

        if (words.length == 0 || transcript.trim().isEmpty()) {
            return chunks;
        }

        // 2. Define overlap (50 words helps maintain context across splits)
        int overlapWords = 50;
        if (overlapWords >= maxWordsPerChunk) {
            overlapWords = maxWordsPerChunk / 2;
        }

        int currentIndex = 0;

        // 3. Sliding window loop
        while (currentIndex < words.length) {
            int endIndex = Math.min(currentIndex + maxWordsPerChunk, words.length);

            StringBuilder chunkBuilder = new StringBuilder();
            for (int i = currentIndex; i < endIndex; i++) {
                chunkBuilder.append(words[i]).append(" ");
            }
            chunks.add(chunkBuilder.toString().trim());

            // If we've reached the end of the array, break to prevent infinite loops
            if (endIndex == words.length) {
                break;
            }

            // 4. Slide window forward minus the overlap
            currentIndex += (maxWordsPerChunk - overlapWords);
        }

        return chunks;
    }

    private Mono<List<Double>> fillFallbackScores(int size) {
        Double[] fallback = new Double[size];
        Arrays.fill(fallback, 10.0);
        return Mono.just(Arrays.asList(fallback));
    }
}