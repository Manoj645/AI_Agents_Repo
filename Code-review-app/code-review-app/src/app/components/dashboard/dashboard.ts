import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { MatCardModule } from '@angular/material/card';
import { MatIconModule } from '@angular/material/icon';
import { MatButtonModule } from '@angular/material/button';
import { MatListModule } from '@angular/material/list';
import { MatChipsModule } from '@angular/material/chips';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { MatSnackBar } from '@angular/material/snack-bar';
import { PullRequest } from '../../models/pull-request.interface';
import { ApiService } from '../../services/api.service';

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [
    CommonModule, 
    RouterModule, 
    MatCardModule, 
    MatIconModule, 
    MatButtonModule, 
    MatListModule, 
    MatChipsModule,
    MatProgressSpinnerModule
  ],
  templateUrl: './dashboard.html',
  styleUrl: './dashboard.scss'
})
export class DashboardComponent implements OnInit {
  prCount: number = 0;
  reviewCount: number = 0;
  suggestionCount: number = 0;
  recentPRs: PullRequest[] = [];
  openPRs: PullRequest[] = [];
  loading: boolean = true;
  error: string = '';

  constructor(
    private apiService: ApiService,
    private snackBar: MatSnackBar
  ) {}

  ngOnInit() {
    this.loadDashboardData();
  }

  loadDashboardData() {
    this.loading = true;
    this.error = '';

    // Fetch all pull requests
    this.apiService.getPullRequests().subscribe({
      next: (prs: PullRequest[]) => {
        this.prCount = prs.length;
        
        // Filter open PRs
        this.openPRs = prs.filter(pr => pr.status === 'open');
        
        // Get recent PRs (last 5)
        this.recentPRs = prs
          .sort((a, b) => new Date(b.created_at).getTime() - new Date(a.created_at).getTime())
          .slice(0, 5);

        // TODO: Fetch review and suggestion counts from API
        this.reviewCount = this.openPRs.length; // Placeholder
        this.suggestionCount = this.openPRs.length * 2; // Placeholder

        this.loading = false;
      },
      error: (error) => {
        console.error('Error fetching PRs:', error);
        this.error = 'Failed to load pull requests';
        this.loading = false;
        
        // Show error message
        this.snackBar.open('Error loading data. Please check if the API server is running.', 'Close', {
          duration: 5000
        });
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

  refreshData() {
    this.loadDashboardData();
  }

  triggerReview(prId: number) {
    this.apiService.triggerAiReview(prId).subscribe({
      next: (result) => {
        this.snackBar.open(`AI review triggered for PR #${prId}`, 'Close', {
          duration: 3000
        });
        // Refresh data after a short delay
        setTimeout(() => this.loadDashboardData(), 2000);
      },
      error: (error) => {
        console.error('Error triggering review:', error);
        this.snackBar.open('Failed to trigger AI review', 'Close', {
          duration: 3000
        });
      }
    });
  }
}
