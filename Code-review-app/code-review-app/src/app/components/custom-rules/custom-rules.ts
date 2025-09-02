import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { MatCardModule } from '@angular/material/card';
import { MatIconModule } from '@angular/material/icon';
import { MatButtonModule } from '@angular/material/button';
import { MatTableModule } from '@angular/material/table';
import { MatChipsModule } from '@angular/material/chips';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { MatSnackBar } from '@angular/material/snack-bar';
import { MatTooltipModule } from '@angular/material/tooltip';
import { MatPaginatorModule, PageEvent } from '@angular/material/paginator';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatSelectModule } from '@angular/material/select';
import { MatDialog, MatDialogModule } from '@angular/material/dialog';
import { FormsModule } from '@angular/forms';
import { CustomRulesService, CustomRule } from '../../services/custom-rules.service';
import { UploadRuleDialogComponent } from './upload-rule-dialog/upload-rule-dialog';
import { ViewRuleDialogComponent } from './view-rule-dialog/view-rule-dialog';

@Component({
  selector: 'app-custom-rules',
  standalone: true,
  imports: [
    CommonModule, 
    RouterModule, 
    MatCardModule, 
    MatIconModule, 
    MatButtonModule, 
    MatTableModule,
    MatChipsModule,
    MatProgressSpinnerModule,
    MatTooltipModule,
    MatPaginatorModule,
    MatFormFieldModule,
    MatInputModule,
    MatSelectModule,
    MatDialogModule,
    FormsModule
  ],
  templateUrl: './custom-rules.html',
  styleUrl: './custom-rules.scss'
})
export class CustomRulesComponent implements OnInit {
  allRules: CustomRule[] = [];
  filteredRules: CustomRule[] = [];
  loading: boolean = true;
  error: string = '';
  searchTerm: string = '';
  selectedLanguage: string = 'all';
  selectedCategory: string = 'all';
  
  // Pagination
  pageSize = 10;
  pageSizeOptions = [5, 10, 25, 50];
  currentPage = 0;
  totalItems = 0;

  // Table columns
  displayedColumns: string[] = ['name', 'language', 'category', 'status', 'updated', 'actions'];

  constructor(
    private customRulesService: CustomRulesService,
    private snackBar: MatSnackBar,
    private dialog: MatDialog
  ) {
    console.log('CustomRulesComponent constructor called');
  }

  ngOnInit() {
    this.loadCustomRules();
  }

  loadCustomRules() {
    this.loading = true;
    this.error = '';
    console.log('Loading custom rules...');

    this.customRulesService.getCustomRules().subscribe({
      next: (rules: CustomRule[]) => {
        console.log('Received rules:', rules);
        this.allRules = rules;
        this.applyFilters();
        this.loading = false;
      },
      error: (error) => {
        console.error('Error fetching custom rules:', error);
        this.error = 'Failed to load custom rules';
        this.loading = false;
        
        // Use mock data for development
        this.allRules = this.customRulesService.getMockCustomRules();
        this.applyFilters();
        this.loading = false;
        
        this.snackBar.open('Using mock data. Please check if the API server is running.', 'Close', {
          duration: 5000
        });
      }
    });
  }

  applyFilters() {
    let filtered = this.allRules;

    // Filter by language
    if (this.selectedLanguage !== 'all') {
      filtered = filtered.filter(rule => rule.language === this.selectedLanguage);
    }

    // Filter by category
    if (this.selectedCategory !== 'all') {
      filtered = filtered.filter(rule => rule.category === this.selectedCategory);
    }

    // Filter by search term
    if (this.searchTerm.trim()) {
      const search = this.searchTerm.toLowerCase();
      filtered = filtered.filter(rule => 
        rule.name.toLowerCase().includes(search) ||
        rule.filename.toLowerCase().includes(search) ||
        rule.language.toLowerCase().includes(search) ||
        rule.category.toLowerCase().includes(search) ||
        rule.content.toLowerCase().includes(search)
      );
    }

    this.filteredRules = filtered;
    this.totalItems = filtered.length;
    this.currentPage = 0;
  }

  onSearchChange() {
    this.applyFilters();
  }

  onLanguageChange() {
    this.applyFilters();
  }

  onCategoryChange() {
    this.applyFilters();
  }

  onPageChange(event: PageEvent) {
    this.currentPage = event.pageIndex;
    this.pageSize = event.pageSize;
  }

  getPaginatedRules(): CustomRule[] {
    const startIndex = this.currentPage * this.pageSize;
    return this.filteredRules.slice(startIndex, startIndex + this.pageSize);
  }

  getLanguageColor(language: string): string {
    const colorMap: { [key: string]: string } = {
      'Python': 'primary',
      'JavaScript': 'accent',
      'TypeScript': 'accent',
      'Java': 'warn',
      'C++': 'warn',
      'C#': 'primary',
      'PHP': 'accent',
      'Go': 'primary',
      'Rust': 'warn'
    };
    
    return colorMap[language] || 'default';
  }

  getCategoryColor(category: string): string {
    const colorMap: { [key: string]: string } = {
      'Style': 'primary',
      'Security': 'warn',
      'Performance': 'accent',
      'Documentation': 'primary',
      'Testing': 'accent',
      'General': 'default'
    };
    
    return colorMap[category] || 'default';
  }

  openUploadDialog() {
    const dialogRef = this.dialog.open(UploadRuleDialogComponent, {
      width: '600px',
      maxWidth: '90vw',
      disableClose: true
    });

    dialogRef.afterClosed().subscribe(result => {
      if (result) {
        // Add the new rule to the list
        this.allRules.unshift(result);
        this.applyFilters();
        
        this.snackBar.open('Custom rule uploaded successfully', 'Close', {
          duration: 3000
        });
      }
    });
  }

  openCreateDialog() {
    // TODO: Implement create rule dialog
    this.snackBar.open('Create rule dialog will be implemented', 'Close', {
      duration: 3000
    });
  }

  viewRule(rule: CustomRule) {
    const dialogRef = this.dialog.open(ViewRuleDialogComponent, {
      width: '800px',
      maxWidth: '90vw',
      maxHeight: '90vh',
      data: { rule: rule }
    });

    dialogRef.afterClosed().subscribe(result => {
      // Dialog closed
    });
  }

  editRule(rule: CustomRule) {
    // TODO: Implement edit rule dialog
    this.snackBar.open(`Editing rule: ${rule.name}`, 'Close', {
      duration: 3000
    });
  }

  toggleRuleStatus(rule: CustomRule) {
    const newStatus = !rule.is_active;
    const action = newStatus ? 'activated' : 'deactivated';
    
    // Update the rule in the local array
    const index = this.allRules.findIndex(r => r.filename === rule.filename);
    if (index !== -1) {
      this.allRules[index].is_active = newStatus;
      this.applyFilters();
    }
    
    this.snackBar.open(`Rule ${action} successfully`, 'Close', {
      duration: 3000
    });
  }

  deleteRule(rule: CustomRule) {
    if (confirm(`Are you sure you want to delete "${rule.name}"?`)) {
      this.customRulesService.deleteCustomRule(rule.filename).subscribe({
        next: (success) => {
          if (success) {
            // Remove the rule from the local array
            this.allRules = this.allRules.filter(r => r.filename !== rule.filename);
            this.applyFilters();
            
            this.snackBar.open('Rule deleted successfully', 'Close', {
              duration: 3000
            });
          }
        },
        error: (error) => {
          console.error('Error deleting rule:', error);
          this.snackBar.open('Failed to delete rule', 'Close', {
            duration: 3000
          });
        }
      });
    }
  }


}
