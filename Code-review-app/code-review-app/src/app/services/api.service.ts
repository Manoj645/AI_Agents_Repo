import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, map } from 'rxjs';
import { PullRequest, CodeReviewSuggestion } from '../models/pull-request.interface';

interface ApiResponse<T> {
  status: string;
  data: T;
  message?: string;
}

@Injectable({
  providedIn: 'root'
})
export class ApiService {
  private baseUrl = 'http://localhost:8000'; // Your FastAPI server URL

  constructor(private http: HttpClient) { }

  // Get all pull requests
  getPullRequests(): Observable<PullRequest[]> {
    return this.http.get<ApiResponse<PullRequest[]>>(`${this.baseUrl}/prs`).pipe(
      map(response => response.data)
    );
  }

  // Get a specific pull request by ID
  getPullRequest(id: number): Observable<PullRequest> {
    return this.http.get<ApiResponse<PullRequest>>(`${this.baseUrl}/prs/${id}`).pipe(
      map(response => response.data)
    );
  }

  // Get files for a specific PR
  getPrFiles(prId: number): Observable<any[]> {
    return this.http.get<ApiResponse<any[]>>(`${this.baseUrl}/prs/${prId}/files`).pipe(
      map(response => response.data)
    );
  }

  // Trigger AI review for a PR
  triggerAiReview(prId: number): Observable<any> {
    return this.http.post(`${this.baseUrl}/trigger-ai-review/${prId}`, {});
  }

  // Check existing reviews for a PR
  checkReviews(prId: number): Observable<any> {
    return this.http.get(`${this.baseUrl}/check-reviews/${prId}`);
  }

  // Get AI configuration status
  getAiConfigStatus(): Observable<any> {
    return this.http.get(`${this.baseUrl}/ai-config-test`);
  }

  // Test GitHub authentication
  testGitHubAuth(token: string, owner: string, repo: string, pr: number): Observable<any> {
    return this.http.get(`${this.baseUrl}/github-auth-test`, {
      params: { token, owner, repo, pr: pr.toString() }
    });
  }
}
