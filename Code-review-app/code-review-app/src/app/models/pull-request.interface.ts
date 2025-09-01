export interface PullRequest {
  id: number;
  title: string;
  description?: string;
  status: 'open' | 'closed' | 'merged';
  author: string;
  repository: string;
  pr_number: number;
  created_at: string;
  updated_at?: string;
  html_url?: string;
  files?: FileChange[];
  suggestions?: CodeReviewSuggestion[];
}

export interface FileChange {
  id: number;
  filename: string;
  file_path: string;
  status: 'added' | 'modified' | 'deleted';
  additions: number;
  deletions: number;
  changes: number;
  pull_request_id: number;
  created_at: string;
}

export interface CodeReviewSuggestion {
  id: number;
  file_path: string;
  line_number?: number;
  suggestion_type: 'improvement' | 'bug' | 'style' | 'security' | 'performance' | 'documentation' | 'testing';
  severity: 'low' | 'medium' | 'high' | 'critical';
  title: string;
  description: string;
  suggestion?: string;
  github_url: string;
  rule_applied: string;
  context_lines?: string;
}
