package com.ltm.backend.Data;

import lombok.Data;

import java.util.List;

@Data
public class MCQ {
    private String question;
    private List<String> options;
    private String correctAnswer;
}
