// This file is the phone the website uses to talk to the server, plus the shapes of the messages they share.

import axios from "axios";

// The server address. It uses the public setting, or the local server if that setting is missing.
const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

// The shared caller that sends every request to that server address.
const api = axios.create({
  baseURL: API_BASE,
});

// Before each request, attach the saved login pass if the person is in the browser and already logged in.
api.interceptors.request.use((config) => {
  if (typeof window !== "undefined") {
    const token = localStorage.getItem("token");
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
  }
  return config;
});

export default api;

// One interview question: the words, the subject, how hard it is, and the ideas a good answer should cover.
export interface Question {
  id?: number;
  question_text: string;
  topic: string;
  difficulty: string;
  expected_concepts?: string[];
}

// The grade for one answer: subject, score, missing ideas, and a short note.
export interface ScoreResult {
  topic: string;
  score: number;
  missing_concepts: string[];
  feedback: string;
}

// What the server sends back after login or signup.
export interface AuthResponse {
  access_token: string;
  user_id: number;
  email: string;
  name: string;
}

// What the server sends back when an interview starts.
export interface StartInterviewResponse {
  session_id: number;
  question: Question;
  question_number: number;
  total_questions: number;
}

// What the server sends back after an answer: the score, and either the next question or the final plan.
export interface AnswerResponse {
  interview_complete: boolean;
  last_score: ScoreResult;
  question?: Question;
  question_number?: number;
  total_questions?: number;
  topic_breakdown?: Record<string, number>;
  focus_recommendations?: string[];
}

// The resume summary the server returns after it reads an uploaded PDF.
export interface ResumeData {
  resume_id: number;
  parsed_data: {
    skills: string[];
    projects: { name: string; description: string }[];
    experience_level: string;
    gaps: string[];
  };
}
