import { Routes } from '@angular/router';
import { DashboardComponent } from './components/dashboard/dashboard.component';
import { PrListComponent } from './components/pr-list/pr-list.component';
import { PrDetailComponent } from './components/pr-detail/pr-detail.component';
import { CodeReviewComponent } from './components/code-review/code-review.component';

export const routes: Routes = [
  { path: '', component: DashboardComponent },
  { path: 'prs', component: PrListComponent },
  { path: 'prs/:id', component: PrDetailComponent },
  { path: 'reviews', component: CodeReviewComponent },
  { path: '**', redirectTo: '' }
];
