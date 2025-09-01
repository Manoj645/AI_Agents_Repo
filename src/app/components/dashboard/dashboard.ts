import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { MatCardModule } from '@angular/material/card';
import { MatIconModule } from '@angular/material/icon';
import { MatButtonModule } from '@angular/material/button';
import { MatListModule } from '@angular/material/list';
import { MatChipsModule } from '@angular/material/chips';
import { PullRequest } from '../../models/pull-request.interface';

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
    MatChipsModule
  ],
  templateUrl: './dashboard.html',
  styleUrl: './dashboard.scss'
})
export class DashboardComponent implements OnInit {
  prCount: number = 0;
  reviewCount: number = 0;
  suggestionCount: number = 0;
  recentPRs: PullRequest[] = [];

  ngOnInit() {
    this.loadDashboardData();
  }

  loadDashboardData() {
    // TODO: Load data from services
    // For now, using mock data
    this.prCount = 7;
    this.reviewCount = 14;
    this.suggestionCount = 23;
    
    this.recentPRs = [
      {
        id: 7,
        title: 'Fix AI agent parser issue',
        description: 'Resolved parser not extracting suggestion details',
        status: 'open',
        author: 'manojkumar.t',
        repository: 'AI_Agents_Repo',
        pr_number: 14,
        created_at: '2025-09-01T21:30:00Z',
        updated_at: '2025-09-01T21:30:00Z'
      },
      {
        id: 6,
        title: 'Add enhanced debugging to code analyzer',
        description: 'Improved logging and error handling',
        status: 'merged',
        author: 'manojkumar.t',
        repository: 'AI_Agents_Repo',
        pr_number: 13,
        created_at: '2025-09-01T20:15:00Z',
        updated_at: '2025-09-01T20:15:00Z'
      }
    ];
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
}
