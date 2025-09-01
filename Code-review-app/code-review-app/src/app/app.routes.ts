import { Routes } from '@angular/router';
import { DashboardComponent } from './components/dashboard/dashboard';
import { PrListComponent } from './components/pr-list/pr-list';
import { PrDetailComponent } from './components/pr-detail/pr-detail';
import { CodeReviewComponent } from './components/code-review/code-review';

export const routes: Routes = [
  { path: '', component: DashboardComponent },
  { path: 'dashboard', component: DashboardComponent },
  { path: 'prs', component: PrListComponent },
  { path: 'prs/:id', component: PrDetailComponent },
  { path: 'reviews', component: CodeReviewComponent },
  { path: '**', redirectTo: '' }
];
