package com.ltm.backend.Data;

import lombok.Data;

import java.util.ArrayList;
import java.util.List;

@Data
public class MCQ_response {
    private List<MCQ> response=new ArrayList<>();
    private String provider;

    public MCQ_response(List<MCQ> mcqs, String provider) {
        this.response=mcqs;
        this.provider=provider;
    }

    public String toString(){
        StringBuilder s=new StringBuilder();
        for(MCQ i:response){
            s.append(i);
        }
        return s.toString();
    }
}
