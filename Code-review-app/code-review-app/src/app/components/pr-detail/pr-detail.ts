import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule, ActivatedRoute } from '@angular/router';
import { MatCardModule } from '@angular/material/card';
import { MatIconModule } from '@angular/material/icon';
import { MatButtonModule } from '@angular/material/button';
import { MatListModule } from '@angular/material/list';
import { MatChipsModule } from '@angular/material/chips';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { MatSnackBar } from '@angular/material/snack-bar';
import { MatTooltipModule } from '@angular/material/tooltip';
import { MatExpansionModule } from '@angular/material/expansion';
import { MatDividerModule } from '@angular/material/divider';
import { PullRequest, CodeReviewSuggestion } from '../../models/pull-request.interface';
import { ApiService } from '../../services/api.service';

@Component({
  selector: 'app-pr-detail',
  standalone: true,
  imports: [
    CommonModule, 
    RouterModule, 
    MatCardModule, 
    MatIconModule, 
    MatButtonModule, 
    MatListModule, 
    MatChipsModule,
    MatProgressSpinnerModule,
    MatTooltipModule,
    MatExpansionModule,
    MatDividerModule
  ],
  templateUrl: './pr-detail.html',
  styleUrl: './pr-detail.scss'
})
export class PrDetailComponent implements OnInit {
  prId: number = 0;
  pullRequest: PullRequest | null = null;
  codeReviews: CodeReviewSuggestion[] = [];
  loading: boolean = true;
  error: string = '';

  constructor(
    private route: ActivatedRoute,
    private apiService: ApiService,
    private snackBar: MatSnackBar
  ) {}

  ngOnInit() {
    this.route.params.subscribe(params => {
      this.prId = +params['id'];
      this.loadPrDetails();
    });
  }

  loadPrDetails() {
    this.loading = true;
    this.error = '';

    // Load PR details
    this.apiService.getPullRequest(this.prId).subscribe({
      next: (pr: PullRequest) => {
        this.pullRequest = pr;
        this.loadCodeReviews();
      },
      error: (error) => {
        console.error('Error fetching PR details:', error);
        this.error = 'Failed to load pull request details';
        this.loading = false;
        
        this.snackBar.open('Error loading PR details', 'Close', {
          duration: 5000
        });
      }
    });
  }

  loadCodeReviews() {
    this.apiService.checkReviews(this.prId).subscribe({
      next: (response: any) => {
        if (response.status === 'success' && response.data) {
          this.codeReviews = response.data;
        } else {
          this.codeReviews = [];
        }
        this.loading = false;
      },
      error: (error) => {
        console.error('Error fetching code reviews:', error);
        this.codeReviews = [];
        this.loading = false;
      }
    });
  }

  getStatusColor(status: string): string {
    switch (status) {
      case 'open':
        return 'primary';
      case 'closed':
        return 'warn';
      case 'merged':
        return 'accent';
      default:
        return 'default';
    }
  }

  getSeverityColor(severity: string): string {
    switch (severity) {
      case 'critical':
        return 'warn';
      case 'high':
        return 'accent';
      case 'medium':
        return 'primary';
      case 'low':
        return 'default';
      default:
        return 'default';
    }
  }

  getTypeIcon(type: string): string {
    switch (type) {
      case 'security':
        return 'security';
      case 'bug':
        return 'bug_report';
      case 'performance':
        return 'speed';
      case 'style':
        return 'style';
      case 'documentation':
        return 'description';
      case 'testing':
        return 'test';
      case 'improvement':
        return 'lightbulb';
      default:
        return 'info';
    }
  }

  triggerReview() {
    this.apiService.triggerAiReview(this.prId).subscribe({
      next: (result) => {
        this.snackBar.open(`AI review triggered for PR #${this.prId}`, 'Close', {
          duration: 3000
        });
        // Refresh reviews after a short delay
        setTimeout(() => this.loadCodeReviews(), 2000);
      },
      error: (error) => {
        console.error('Error triggering review:', error);
        this.snackBar.open('Failed to trigger AI review', 'Close', {
          duration: 3000
        });
      }
    });
  }

  refreshData() {
    this.loadPrDetails();
  }

  getReviewsBySeverity(severity: string): CodeReviewSuggestion[] {
    return this.codeReviews.filter(review => review.severity === severity);
  }

  getReviewsByType(type: string): CodeReviewSuggestion[] {
    return this.codeReviews.filter(review => review.suggestion_type === type);
  }
}
