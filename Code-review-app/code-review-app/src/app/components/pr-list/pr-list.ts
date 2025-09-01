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
import { MatTooltipModule } from '@angular/material/tooltip';
import { MatPaginatorModule, PageEvent } from '@angular/material/paginator';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatSelectModule } from '@angular/material/select';
import { FormsModule } from '@angular/forms';
import { PullRequest } from '../../models/pull-request.interface';
import { ApiService } from '../../services/api.service';

@Component({
  selector: 'app-pr-list',
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
    MatPaginatorModule,
    MatFormFieldModule,
    MatInputModule,
    MatSelectModule,
    FormsModule
  ],
  templateUrl: './pr-list.html',
  styleUrl: './pr-list.scss'
})
export class PrListComponent implements OnInit {
  allPRs: PullRequest[] = [];
  filteredPRs: PullRequest[] = [];
  openPRs: PullRequest[] = [];
  loading: boolean = true;
  error: string = '';
  searchTerm: string = '';
  selectedStatus: string = 'all';
  
  // Pagination
  pageSize = 10;
  pageSizeOptions = [5, 10, 25, 50];
  currentPage = 0;
  totalItems = 0;

  constructor(
    private apiService: ApiService,
    private snackBar: MatSnackBar
  ) {}

  ngOnInit() {
    this.loadPullRequests();
  }

  loadPullRequests() {
    this.loading = true;
    this.error = '';

    this.apiService.getPullRequests().subscribe({
      next: (prs: PullRequest[]) => {
        this.allPRs = prs;
        this.openPRs = prs.filter(pr => pr.status === 'open');
        this.applyFilters();
        this.loading = false;
      },
      error: (error) => {
        console.error('Error fetching PRs:', error);
        this.error = 'Failed to load pull requests';
        this.loading = false;
        
        this.snackBar.open('Error loading data. Please check if the API server is running.', 'Close', {
          duration: 5000
        });
      }
    });
  }

  applyFilters() {
    let filtered = this.allPRs;

    // Filter by status
    if (this.selectedStatus !== 'all') {
      filtered = filtered.filter(pr => pr.status === this.selectedStatus);
    }

    // Filter by search term
    if (this.searchTerm.trim()) {
      const search = this.searchTerm.toLowerCase();
      filtered = filtered.filter(pr => 
        pr.title.toLowerCase().includes(search) ||
        pr.author.toLowerCase().includes(search) ||
        pr.repository.toLowerCase().includes(search) ||
        (pr.description && pr.description.toLowerCase().includes(search))
      );
    }

    this.filteredPRs = filtered;
    this.totalItems = filtered.length;
    this.currentPage = 0;
  }

  onSearchChange() {
    this.applyFilters();
  }

  onStatusChange() {
    this.applyFilters();
  }

  onPageChange(event: PageEvent) {
    this.currentPage = event.pageIndex;
    this.pageSize = event.pageSize;
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

  triggerReview(prId: number) {
    this.apiService.triggerAiReview(prId).subscribe({
      next: (result) => {
        this.snackBar.open(`AI review triggered for PR #${prId}`, 'Close', {
          duration: 3000
        });
        // Refresh data after a short delay
        setTimeout(() => this.loadPullRequests(), 2000);
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
    this.loadPullRequests();
  }

  getPaginatedPRs(): PullRequest[] {
    const startIndex = this.currentPage * this.pageSize;
    return this.filteredPRs.slice(startIndex, startIndex + this.pageSize);
  }

  getStatusCount(status: string): number {
    return this.allPRs.filter(pr => pr.status === status).length;
  }

  getTotalAdditions(pr: PullRequest): number {
    return pr.files ? pr.files.reduce((total, file) => total + file.additions, 0) : 0;
  }

  getTotalDeletions(pr: PullRequest): number {
    return pr.files ? pr.files.reduce((total, file) => total + file.deletions, 0) : 0;
  }
}
