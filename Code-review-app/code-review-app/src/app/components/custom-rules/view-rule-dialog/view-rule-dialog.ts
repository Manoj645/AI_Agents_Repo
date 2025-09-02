import { Component, Inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MatDialogRef, MAT_DIALOG_DATA, MatDialogModule } from '@angular/material/dialog';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MatChipsModule } from '@angular/material/chips';
import { CustomRule } from '../../../services/custom-rules.service';

@Component({
  selector: 'app-view-rule-dialog',
  standalone: true,
  imports: [
    CommonModule,
    MatDialogModule,
    MatButtonModule,
    MatIconModule,
    MatChipsModule
  ],
  templateUrl: './view-rule-dialog.html',
  styleUrl: './view-rule-dialog.scss'
})
export class ViewRuleDialogComponent {
  rule: CustomRule;

  constructor(
    public dialogRef: MatDialogRef<ViewRuleDialogComponent>,
    @Inject(MAT_DIALOG_DATA) public data: { rule: CustomRule }
  ) {
    this.rule = data.rule;
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
      'Rust': 'warn',
      'Markdown': 'primary',
      'Text': 'default'
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

  downloadFile() {
    const blob = new Blob([this.rule.content], { type: 'text/plain' });
    const url = window.URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = this.rule.filename;
    link.click();
    window.URL.revokeObjectURL(url);
  }

  onClose(): void {
    this.dialogRef.close();
  }
}
