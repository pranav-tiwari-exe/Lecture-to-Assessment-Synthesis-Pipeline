package com.ltm.backend.Data;

import lombok.Data;

@Data
public class TranscriptRequest {
    private String transcript;
    private String youtubeUrl;
    private int questions;
}
