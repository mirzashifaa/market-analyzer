import axios, { AxiosError } from "axios";
import type { AnalysisRequest, AnalysisResponse } from "./types";

const client = axios.create({
  baseURL: import.meta.env.VITE_API_URL || "http://localhost:8000",
  headers: { "Content-Type": "application/json" },
  timeout: 120000, // 2 minute timeout
});

export async function analyze(
  request: AnalysisRequest
): Promise<AnalysisResponse> {
  try {
    const response = await client.post<AnalysisResponse>(
      "/analyze",
      request
    );
    return response.data;
  } catch (err) {
    const error = err as AxiosError<{ detail: string }>;
    if (error.response?.status === 429) {
      throw new Error(
        "Rate limit reached. Please wait 30 seconds and try again."
      );
    }
    if (error.response?.status === 400) {
      throw new Error(
        error.response.data?.detail ||
          "Market is too broad. Please provide a more specific category."
      );
    }
    if (error.response?.status === 500) {
      throw new Error(
        error.response.data?.detail || 
        "Analysis failed. Please try again."
      );
    }
    if (error.code === "ECONNABORTED") {
      throw new Error(
        "Analysis timed out. Please try again."
      );
    }
    throw new Error("Something went wrong. Please try again.");
  }
}