import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, of } from 'rxjs';
import { map, catchError } from 'rxjs/operators';

export interface CustomRule {
  id: string;
  name: string;
  filename: string;
  content: string;
  language: string;
  category: string;
  created_at: string;
  updated_at: string;
  is_active: boolean;
}

export interface CustomRuleFile {
  name: string;
  content: string;
  language: string;
  category: string;
}

@Injectable({
  providedIn: 'root'
})
export class CustomRulesService {
  private apiUrl = 'http://localhost:8000'; // Adjust based on your API

  constructor(private http: HttpClient) {}

  // Get all custom rules
  getCustomRules(): Observable<CustomRule[]> {
    console.log('Making API call to:', `${this.apiUrl}/custom-rules`);
    return this.http.get<{status: string, data: CustomRule[]}>(`${this.apiUrl}/custom-rules`).pipe(
      map(response => {
        console.log('API response:', response);
        return response.data;
      }),
      catchError(error => {
        console.error('Error fetching custom rules:', error);
        return of([]);
      })
    );
  }

  // Get a specific custom rule by ID
  getCustomRule(id: string): Observable<CustomRule | null> {
    return this.http.get<{status: string, data: CustomRule}>(`${this.apiUrl}/custom-rules/${id}`).pipe(
      map(response => response.data),
      catchError(error => {
        console.error('Error fetching custom rule:', error);
        return of(null);
      })
    );
  }

  // Create a new custom rule
  createCustomRule(rule: CustomRuleFile): Observable<CustomRule | null> {
    return this.http.post<{status: string, data: CustomRule}>(`${this.apiUrl}/custom-rules`, rule).pipe(
      map(response => response.data),
      catchError(error => {
        console.error('Error creating custom rule:', error);
        return of(null);
      })
    );
  }

  // Update an existing custom rule
  updateCustomRule(id: string, rule: Partial<CustomRule>): Observable<CustomRule | null> {
    return this.http.put<{status: string, data: CustomRule}>(`${this.apiUrl}/custom-rules/${id}`, rule).pipe(
      map(response => response.data),
      catchError(error => {
        console.error('Error updating custom rule:', error);
        return of(null);
      })
    );
  }

  // Delete a custom rule
  deleteCustomRule(filename: string): Observable<boolean> {
    return this.http.delete(`${this.apiUrl}/custom-rules/${filename}`).pipe(
      map(() => true),
      catchError(error => {
        console.error('Error deleting custom rule:', error);
        return of(false);
      })
    );
  }

  // Upload a file and create custom rule
  uploadCustomRule(file: File): Observable<CustomRule | null> {
    const formData = new FormData();
    formData.append('file', file);
    
    return this.http.post<{status: string, data: CustomRule}>(`${this.apiUrl}/custom-rules/upload`, formData).pipe(
      map(response => response.data),
      catchError(error => {
        console.error('Error uploading custom rule:', error);
        return of(null);
      })
    );
  }

  // Parse file content to extract rule information
  parseRuleFile(content: string, filename: string): CustomRuleFile {
    const language = this.detectLanguage(filename);
    const category = this.detectCategory(content);
    
    return {
      name: filename.replace(/\.[^/.]+$/, ''), // Remove file extension
      content: content,
      language: language,
      category: category
    };
  }

  // Detect programming language from filename
  private detectLanguage(filename: string): string {
    const extension = filename.split('.').pop()?.toLowerCase();
    const languageMap: { [key: string]: string } = {
      'py': 'Python',
      'js': 'JavaScript',
      'ts': 'TypeScript',
      'java': 'Java',
      'cpp': 'C++',
      'c': 'C',
      'cs': 'C#',
      'php': 'PHP',
      'rb': 'Ruby',
      'go': 'Go',
      'rs': 'Rust',
      'md': 'Markdown',
      'txt': 'Text'
    };
    
    return languageMap[extension || ''] || 'Unknown';
  }

  // Detect category from content
  private detectCategory(content: string): string {
    const lowerContent = content.toLowerCase();
    
    if (lowerContent.includes('security') || lowerContent.includes('vulnerability')) {
      return 'Security';
    } else if (lowerContent.includes('performance') || lowerContent.includes('optimization')) {
      return 'Performance';
    } else if (lowerContent.includes('style') || lowerContent.includes('formatting')) {
      return 'Style';
    } else if (lowerContent.includes('documentation') || lowerContent.includes('comment')) {
      return 'Documentation';
    } else if (lowerContent.includes('test') || lowerContent.includes('testing')) {
      return 'Testing';
    } else {
      return 'General';
    }
  }

  // Get mock data for development
  getMockCustomRules(): CustomRule[] {
    return [
      {
        id: '1',
        name: 'Python Code Standards',
        filename: 'python-code-standards.md',
        content: '# Python Code Standards\n\n## Code Quality Rules\n\n### Function Length & Complexity\n- Functions should not exceed 15 lines of code\n- Improves readability and maintainability',
        language: 'Python',
        category: 'Style',
        created_at: '2024-01-15T10:00:00Z',
        updated_at: '2024-01-15T10:00:00Z',
        is_active: true
      },
      {
        id: '2',
        name: 'JavaScript Best Practices',
        filename: 'javascript-standards.md',
        content: '# JavaScript Best Practices\n\n## Code Quality Rules\n\n### Variable Naming\n- Use camelCase for variables and functions\n- Use PascalCase for classes',
        language: 'JavaScript',
        category: 'Style',
        created_at: '2024-01-16T10:00:00Z',
        updated_at: '2024-01-16T10:00:00Z',
        is_active: true
      }
    ];
  }
}
