import { Component, Inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MatDialogRef, MAT_DIALOG_DATA, MatDialogModule } from '@angular/material/dialog';
import { MatIconModule } from '@angular/material/icon';
import { MatButtonModule } from '@angular/material/button';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatSelectModule } from '@angular/material/select';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { MatTooltipModule } from '@angular/material/tooltip';
import { FormsModule } from '@angular/forms';
import { CustomRulesService } from '../../../services/custom-rules.service';

@Component({
  selector: 'app-upload-rule-dialog',
  standalone: true,
  imports: [
    CommonModule,
    MatDialogModule,
    MatIconModule,
    MatButtonModule,
    MatFormFieldModule,
    MatInputModule,
    MatSelectModule,
    MatProgressSpinnerModule,
    MatTooltipModule,
    FormsModule
  ],
  templateUrl: './upload-rule-dialog.html',
  styleUrl: './upload-rule-dialog.scss'
})
export class UploadRuleDialogComponent {
  selectedFile: File | null = null;
  fileContent: string = '';
  ruleName: string = '';
  selectedLanguage: string = '';
  selectedCategory: string = '';
  ruleDescription: string = '';
  isDragOver: boolean = false;
  uploading: boolean = false;

  constructor(
    public dialogRef: MatDialogRef<UploadRuleDialogComponent>,
    @Inject(MAT_DIALOG_DATA) public data: any,
    private customRulesService: CustomRulesService
  ) {}

  onDragOver(event: DragEvent) {
    event.preventDefault();
    event.stopPropagation();
    this.isDragOver = true;
  }

  onDragLeave(event: DragEvent) {
    event.preventDefault();
    event.stopPropagation();
    this.isDragOver = false;
  }

  onDrop(event: DragEvent) {
    event.preventDefault();
    event.stopPropagation();
    this.isDragOver = false;

    const files = event.dataTransfer?.files;
    if (files && files.length > 0) {
      this.handleFile(files[0]);
    }
  }

  onFileSelected(event: any) {
    const file = event.target.files[0];
    if (file) {
      this.handleFile(file);
    }
  }

  private handleFile(file: File) {
    // Validate file size (5MB limit)
    if (file.size > 5 * 1024 * 1024) {
      alert('File size must be less than 5MB');
      return;
    }

    // Validate file type
    const allowedExtensions = ['.md', '.txt', '.py', '.js', '.ts', '.java', '.cpp', '.c', '.cs', '.php', '.rb', '.go', '.rs'];
    const fileExtension = '.' + file.name.split('.').pop()?.toLowerCase();
    
    if (!allowedExtensions.includes(fileExtension)) {
      alert('Unsupported file type. Please upload a supported file format.');
      return;
    }

    this.selectedFile = file;
    this.ruleName = file.name.replace(/\.[^/.]+$/, ''); // Remove file extension
    
    // Auto-detect language and category
    const ruleInfo = this.customRulesService.parseRuleFile('', file.name);
    this.selectedLanguage = ruleInfo.language;
    this.selectedCategory = ruleInfo.category;

    // Read file content
    const reader = new FileReader();
    reader.onload = (e) => {
      this.fileContent = e.target?.result as string;
    };
    reader.readAsText(file);
  }

  removeFile() {
    this.selectedFile = null;
    this.fileContent = '';
    this.ruleName = '';
    this.selectedLanguage = '';
    this.selectedCategory = '';
    this.ruleDescription = '';
  }

  onUpload() {
    if (!this.selectedFile || !this.ruleName || !this.selectedLanguage || !this.selectedCategory) {
      return;
    }

    this.uploading = true;

    // Create rule object
    const ruleData = {
      name: this.ruleName,
      content: this.fileContent,
      language: this.selectedLanguage,
      category: this.selectedCategory,
      description: this.ruleDescription
    };

    // Upload the rule
    this.customRulesService.createCustomRule(ruleData).subscribe({
      next: (result) => {
        this.uploading = false;
        if (result) {
          this.dialogRef.close(result);
        } else {
          alert('Failed to upload rule. Please try again.');
        }
      },
      error: (error) => {
        this.uploading = false;
        console.error('Upload error:', error);
        alert('Failed to upload rule. Please try again.');
      }
    });
  }

  onCancel() {
    this.dialogRef.close();
  }
}
