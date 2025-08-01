import { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Upload, Link2, FileText, CheckCircle2 } from 'lucide-react';
import { useToast } from '@/hooks/use-toast';

interface DocumentUploadProps {
  onDocumentUploaded: (document: { url: string; name: string; type: string }) => void;
}

export const DocumentUpload = ({ onDocumentUploaded }: DocumentUploadProps) => {
  const [documentUrl, setDocumentUrl] = useState('');
  const [isProcessing, setIsProcessing] = useState(false);
  const [uploadedFile, setUploadedFile] = useState<File | null>(null);
  const { toast } = useToast();

  const handleUrlSubmit = async () => {
    if (!documentUrl.trim()) {
      toast({
        title: "Error",
        description: "Please enter a valid document URL",
        variant: "destructive",
      });
      return;
    }

    setIsProcessing(true);
    
    try {
      // For URL-based documents, we'll pass the URL directly
      onDocumentUploaded({
        url: documentUrl,
        name: documentUrl.split('/').pop() || 'Document',
        type: 'url'
      });
      
      toast({
        title: "Success",
        description: "Document URL loaded successfully",
      });
    } catch (error) {
      toast({
        title: "Error",
        description: "Failed to load document from URL",
        variant: "destructive",
      });
    } finally {
      setIsProcessing(false);
    }
  };

  const handleFileUpload = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (!file) return;

    if (!['application/pdf', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'].includes(file.type)) {
      toast({
        title: "Error",
        description: "Please upload a PDF or DOCX file",
        variant: "destructive",
      });
      return;
    }

    setUploadedFile(file);
    setIsProcessing(true);

    try {
      // Create object URL for the file and pass it to the parent component
      const objectUrl = URL.createObjectURL(file);
      onDocumentUploaded({
        url: objectUrl,
        name: file.name,
        type: 'file'
      });
      
      toast({
        title: "Success",
        description: "Document uploaded successfully",
      });
    } catch (error) {
      toast({
        title: "Error",
        description: "Failed to process uploaded file",
        variant: "destructive",
      });
    } finally {
      setIsProcessing(false);
    }
  };

  return (
    <Card className="bg-card/50 backdrop-blur-sm border-border/50 shadow-glass">
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <FileText className="h-5 w-5 text-primary" />
          Document Upload
        </CardTitle>
        <CardDescription>
          Upload or provide a URL to your document for analysis
        </CardDescription>
      </CardHeader>
      <CardContent>
        <Tabs defaultValue="upload" className="w-full">
          <TabsList className="grid w-full grid-cols-2">
            <TabsTrigger value="url" className="flex items-center gap-2">
              <Link2 className="h-4 w-4" />
              URL
            </TabsTrigger>
            <TabsTrigger value="upload" className="flex items-center gap-2">
              <Upload className="h-4 w-4" />
              Upload
            </TabsTrigger>
          </TabsList>
          
          <TabsContent value="url" className="space-y-4">
            <div className="space-y-2">
              <Label htmlFor="document-url">Document URL</Label>
              <Input
                id="document-url"
                placeholder="https://example.com/document.pdf"
                value={documentUrl}
                onChange={(e) => setDocumentUrl(e.target.value)}
                className="bg-background/50"
              />
            </div>
            <Button 
              onClick={handleUrlSubmit}
              disabled={isProcessing}
              className="w-full bg-gradient-primary hover:opacity-90 transition-smooth"
            >
              {isProcessing ? (
                <>
                  <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2" />
                  Processing...
                </>
              ) : (
                <>
                  <Link2 className="h-4 w-4 mr-2" />
                  Load Document
                </>
              )}
            </Button>
          </TabsContent>
          
          <TabsContent value="upload" className="space-y-4">
            <div className="space-y-2">
              <Label htmlFor="document-file">Upload Document</Label>
              <div className="border-2 border-dashed border-border rounded-lg p-8 text-center hover:border-primary/50 transition-smooth">
                <Upload className="h-8 w-8 mx-auto mb-4 text-muted-foreground" />
                <div className="space-y-2">
                  <p className="text-sm text-muted-foreground">
                    Drag and drop or click to select
                  </p>
                  <p className="text-xs text-muted-foreground">
                    Supports PDF and DOCX files
                  </p>
                </div>
                <input
                  id="document-file"
                  type="file"
                  className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
                  accept=".pdf,.docx"
                  onChange={handleFileUpload}
                />
              </div>
              {uploadedFile && (
                <div className="flex items-center gap-2 p-3 bg-success/10 rounded-lg border border-success/20">
                  <CheckCircle2 className="h-4 w-4 text-success" />
                  <span className="text-sm font-medium">{uploadedFile.name}</span>
                </div>
              )}
            </div>
          </TabsContent>
        </Tabs>
      </CardContent>
    </Card>
  );
};