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

@Service("llm2Service")
public class LLM2Service {
    @Value("${llm2Key}")
    private String llm2Key;
    @Value("${llm2Uri}")
    private String llm2Uri;

    private final WebClient webClient;
    private final ObjectMapper objectMapper;

    public LLM2Service(WebClient webClient, ObjectMapper objectMapper){
        this.webClient = webClient;
        this.objectMapper = objectMapper;
    }

    public Mono<MCQ_response> generate(String fullTranscript) {
        // Chunk transcript to max 400 words using sliding window to handle unpunctuated text
        List<String> chunks = chunkTranscript(fullTranscript, 400);

        return Flux.fromIterable(chunks)
                .flatMap(this::generateSingleChunk, 3)
                .reduce(new MCQ_response(new ArrayList<>(), "Groq llama agent"), (mergedResult, nextChunk) -> {
                    if (nextChunk != null && nextChunk.getResponse() != null) {
                        mergedResult.getResponse().addAll(nextChunk.getResponse());
                    }
                    return mergedResult;
                })
                .defaultIfEmpty(new MCQ_response(new ArrayList<>(), "Groq llama agent"));
    }

    private Mono<MCQ_response> generateSingleChunk(String chunk) {
        String prompt = "You are an expert quiz creator. Extract EXHAUSTIVELY from the provided transcript chunk. " +
                "Generate the ABSOLUTE MAXIMUM number of unique, non-repeating MCQs. " +
                "Output MUST be JSON with these keys: 'response' (list of questions) and 'provider'(always 'Groq llama agent'). " +
                "Each question must have 'question', 'options' (list), and 'correctAnswer'.\n\n" +
                "Transcript Chunk: " + chunk;

        Map<String, Object> requestBody = Map.of(
                "model", "llama-3.1-8b-instant",
                "messages", List.of(
                        Map.of("role", "system", "content", "You are a teacher. Always output valid JSON."),
                        Map.of("role", "user", "content", prompt)
                ),
                "response_format", Map.of("type", "json_object")
        );

        return webClient.post()
                .uri(llm2Uri)
                .header("Authorization", "Bearer " + llm2Key)
                .bodyValue(requestBody)
                .retrieve()
                .bodyToMono(JsonNode.class)
                .timeout(Duration.ofSeconds(45))
                .map(jsonResponse -> {
                    try {
                        String jsonString = jsonResponse.path("choices").get(0).path("message").path("content").asText();
                        return objectMapper.readValue(jsonString, MCQ_response.class);
                    } catch (Exception e) {
                        throw new RuntimeException("llm2 Parsing Error: " + e.getMessage());
                    }
                })
                .onErrorResume(e -> Mono.just(new MCQ_response(new ArrayList<>(), "Groq (Failed Chunk)")));
    }

    public Mono<List<Double>> validate(String transcript, MCQ_response response) {
        String prompt = "Analyze the provided transcript and the list of generated MCQs. " +
                "Score each question from 1.0 to 10.0 based on its relevancy. " +
                "If a question is a duplicate, return -1.0. " +
                "Return ONLY a JSON object with a key 'scores' containing an array of numbers.\n\n" +
                "Transcript: " + transcript + "\nMCQs: " + response.toString();

        Map<String, Object> requestBody = Map.of(
                "model", "llama-3.1-8b-instant",
                "messages", List.of(
                        Map.of("role", "system", "content", "You are a precise assistant. Always output valid JSON."),
                        Map.of("role", "user", "content", prompt)
                ),
                "response_format", Map.of("type", "json_object")
        );

        return webClient.post()
                .uri(llm2Uri)
                .header("Authorization", "Bearer " + llm2Key)
                .bodyValue(requestBody)
                .retrieve()
                .bodyToMono(JsonNode.class)
                .timeout(Duration.ofSeconds(45))
                .map(jsonResponse -> {
                    try {
                        String jsonString = jsonResponse.path("choices").get(0).path("message").path("content").asText();
                        JsonNode innerJson = objectMapper.readTree(jsonString);
                        JsonNode scoresNode = innerJson.path("scores");

                        if (scoresNode.isMissingNode()) {
                            throw new RuntimeException("LLM forgot 'scores' key!");
                        }

                        Double[] scoresArray = objectMapper.treeToValue(scoresNode, Double[].class);
                        return Arrays.asList(scoresArray);
                    } catch (Exception e) {
                        throw new RuntimeException("llm2 Validation Error: " + e.getMessage());
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