package com.ltm.backend.services;

import com.ltm.backend.Data.MCQ;
import com.ltm.backend.Data.MCQ_response;
import org.springframework.stereotype.Service;
import reactor.core.publisher.Mono;

import java.util.HashSet;
import java.util.List;
import java.util.Set;

@Service
public class ValidatorService {
    private final LLM1Service llm1Service;
    private final LLM2Service llm2Service;

    public ValidatorService(LLM1Service llm1Service, LLM2Service llm2Service) {
        this.llm1Service = llm1Service;
        this.llm2Service = llm2Service;
    }

    public Mono<MCQ_response> validate(String transcript, MCQ_response mcqs) {
        if (mcqs == null || mcqs.getResponse() == null || mcqs.getResponse().isEmpty()) {
            return Mono.just(mcqs);
        }

        Mono<List<Double>> scoresllm1 = llm1Service.validate(transcript, mcqs);
        Mono<List<Double>> scoresllm2 = llm2Service.validate(transcript, mcqs);

        return Mono.zip(scoresllm1, scoresllm2).map(tuple -> {
            List<Double> l1 = tuple.getT1();
            List<Double> l2 = tuple.getT2();
            Set<Integer> removeIDX = new HashSet<>();

            int totalQuestions = mcqs.getResponse().size();

            for (int j = 0; j < totalQuestions; j++) {
                if (j >= l1.size() || j >= l2.size()) {
                    removeIDX.add(j);
                    continue;
                }

                double s1 = l1.get(j);
                double s2 = l2.get(j);

                if (s1 <= -1.0 || s2 <= -1.0 || (s1 + s2) / 2.0 < 6.5) {
                    removeIDX.add(j);
                }
            }

            List<MCQ> list = mcqs.getResponse();
            for (int k = list.size() - 1; k >= 0; k--) {
                if (removeIDX.contains(k)) {
                    list.remove(k);
                }
            }

            mcqs.setResponse(list);
            return mcqs;
        });
    }
}