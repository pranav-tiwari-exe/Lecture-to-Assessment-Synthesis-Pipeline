package com.ltm.backend.controllers;

import com.ltm.backend.Data.MCQ_response;
import com.ltm.backend.Data.TranscriptRequest;
import com.ltm.backend.services.LLM1Service;
import com.ltm.backend.services.LLM2Service;
import com.ltm.backend.services.ValidatorService;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;
import reactor.core.publisher.Mono;

import java.util.ArrayList;
import java.util.List;

@RestController
//@CrossOrigin (origins = "http://localhost:3000")
public class Generator {

     private final LLM1Service llm1Service;
     private final LLM2Service llm2Service;
     private final ValidatorService validatorService;

     public Generator(LLM1Service llm1Service, LLM2Service llm2Service, ValidatorService validatorService) {
          this.llm1Service = llm1Service;
          this.llm2Service = llm2Service;
          this.validatorService = validatorService;
     }

     @PostMapping("/generate")
     public Mono<ResponseEntity<MCQ_response>> generate(@RequestBody TranscriptRequest request) {

         if ((request.getTranscript() == null || request.getTranscript().isEmpty()) && request.getYoutubeUrl()!=null) {

         }
          String transcript = request.getTranscript();

          Mono<MCQ_response> llm1Mono = llm1Service.generate(transcript);
          Mono<MCQ_response> llm2Mono = llm2Service.generate(transcript);

          return Mono.zip(llm1Mono, llm2Mono).flatMap(tuple -> {

                       MCQ_response mergedMcq = tuple.getT1();
                       if (mergedMcq.getResponse() == null) {
                            mergedMcq.setResponse(new ArrayList<>());
                       }
                       if (tuple.getT2().getResponse() != null) {
                            mergedMcq.getResponse().addAll(tuple.getT2().getResponse());
                       }
                       mergedMcq.setProvider("Hybrid (Gemini + Groq)");

                       return validatorService.validate(transcript, mergedMcq);
                  })
                  .map(ResponseEntity::ok);
     }

     // --- Test Endpoints ---
     @PostMapping("/testllm1")
     public Mono<MCQ_response> generatellm1(@RequestBody TranscriptRequest request) {
          return llm1Service.generate(request.getTranscript());
     }

     @PostMapping("/testllm2")
     public Mono<MCQ_response> generatellm2(@RequestBody TranscriptRequest request) {
          return llm2Service.generate(request.getTranscript());
     }
}