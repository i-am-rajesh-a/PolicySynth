import { useState } from 'react';
import { DocumentUpload } from '@/components/DocumentUpload';
import { QueryInterface } from '@/components/QueryInterface';
import { ResultsDisplay } from '@/components/ResultsDisplay';
import { SystemStatus } from '@/components/SystemStatus';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Brain, Shield, FileSearch, Sparkles } from 'lucide-react';
import { useToast } from '@/hooks/use-toast';

interface Document {
  url: string;
  name: string;
  type: string;
}

interface Evidence {
  clause_id: string;
  text: string;
  similarity_score: number;
  source: string;
  section?: string;
}

interface QueryResult {
  query: string;
  answer: string;
  evidence: Evidence[];
  conditions: string[];
  decision_rationale: string;
  confidence: number;
  status: 'covered' | 'not_covered' | 'conditional' | 'unclear';
  token_usage?: number;
  processing_time?: number;
}

// Use environment variable for API URL, fallback to localhost for development
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000/api/v1';

const Index = () => {
  const [document, setDocument] = useState<Document | null>(null);
  const [isProcessing, setIsProcessing] = useState(false);
  const [currentResult, setCurrentResult] = useState<QueryResult | null>(null);
  const [totalTokensUsed, setTotalTokensUsed] = useState(0);
  const [lastQueryTime, setLastQueryTime] = useState<number | undefined>();
  const { toast } = useToast();

  const handleDocumentUploaded = async (newDocument: Document) => {
    try {
      setIsProcessing(true);
      
      // Create FormData for file upload
      const formData = new FormData();
      const response = await fetch(newDocument.url);
      const blob = await response.blob();
      formData.append('file', blob, newDocument.name);
      
      // Upload document to backend
      const uploadResponse = await fetch(`${API_BASE_URL}/upload/`, {
        method: 'POST',
        body: formData,
      });
      
      if (!uploadResponse.ok) {
        throw new Error('Failed to upload document');
      }
      
      setDocument(newDocument);
      setCurrentResult(null);
      toast({
        title: "Document uploaded successfully",
        description: "Your document has been processed and is ready for analysis.",
      });
    } catch (error) {
      console.error('Upload error:', error);
      toast({
        title: "Upload failed",
        description: "Failed to upload and process the document. Please try again.",
        variant: "destructive",
      });
    } finally {
      setIsProcessing(false);
    }
  };

  const handleQuerySubmit = async (query: string) => {
    if (!document) {
      toast({
        title: "No document uploaded",
        description: "Please upload a document first before asking questions.",
        variant: "destructive",
      });
      return;
    }

    setIsProcessing(true);
    setCurrentResult(null);
    
    const startTime = Date.now();
    
    try {
      const response = await fetch(`${API_BASE_URL}/ask/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ question: query }),
      });
      
      if (!response.ok) {
        throw new Error('Failed to get analysis');
      }
      
      const result: QueryResult = await response.json();
      const processingTime = (Date.now() - startTime) / 1000;
      
      // Add processing time to result
      result.processing_time = processingTime;
      
      setCurrentResult(result);
      setTotalTokensUsed(prev => prev + (result.token_usage || 0));
      setLastQueryTime(processingTime);
      
      toast({
        title: "Analysis complete",
        description: `Analysis completed in ${processingTime.toFixed(2)} seconds.`,
      });
    } catch (error) {
      console.error('Query error:', error);
      toast({
        title: "Analysis failed",
        description: "Failed to analyze your question. Please try again.",
        variant: "destructive",
      });
    } finally {
      setIsProcessing(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-surface">
      {/* Header */}
      <div className="border-b border-border/20 bg-background/50 backdrop-blur-sm">
        <div className="container mx-auto px-4 py-6">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="p-2 bg-gradient-primary rounded-lg">
                <Brain className="h-6 w-6 text-white" />
              </div>
              <div>
                <h1 className="text-2xl font-bold bg-gradient-primary bg-clip-text text-transparent">
                  Policy Scanner
                </h1>
                <p className="text-sm text-muted-foreground">
                  AI-Powered Policy Analysis System
                </p>
              </div>
            </div>
            <div className="flex items-center gap-2">
              <Badge variant="secondary" className="flex items-center gap-1">
                <Shield className="h-3 w-3" />
                Secure
              </Badge>
              <Badge variant="outline" className="flex items-center gap-1">
                <Sparkles className="h-3 w-3" />
                AI-Powered
              </Badge>
            </div>
          </div>
        </div>
      </div>

      <div className="container mx-auto px-4 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Left Column - Controls */}
          <div className="lg:col-span-1 space-y-6">
            <DocumentUpload onDocumentUploaded={handleDocumentUploaded} />
            <QueryInterface 
              onQuerySubmit={handleQuerySubmit}
              isProcessing={isProcessing}
              hasDocument={!!document}
            />
            <SystemStatus
              hasDocument={!!document}
              isProcessing={isProcessing}
              lastQueryTime={lastQueryTime}
              tokensUsed={totalTokensUsed}
            />
          </div>

          {/* Right Column - Results */}
          <div className="lg:col-span-2">
            <ResultsDisplay 
              result={currentResult}
              isLoading={isProcessing}
            />
          </div>
        </div>

        {/* Feature Cards */}
        <div className="mt-12 grid grid-cols-1 md:grid-cols-3 gap-6">
          <Card className="bg-card/30 backdrop-blur-sm border-border/50">
            <CardHeader>
              <CardTitle className="flex items-center gap-2 text-lg">
                <FileSearch className="h-5 w-5 text-primary" />
                Intelligent Search
              </CardTitle>
            </CardHeader>
            <CardContent>
              <CardDescription>
                Advanced AI-powered search finds relevant information across your documents
              </CardDescription>
            </CardContent>
          </Card>

          <Card className="bg-card/30 backdrop-blur-sm border-border/50">
            <CardHeader>
              <CardTitle className="flex items-center gap-2 text-lg">
                <Brain className="h-5 w-5 text-primary" />
                Explainable Analysis
              </CardTitle>
            </CardHeader>
            <CardContent>
              <CardDescription>
                Get clear explanations with supporting evidence for every analysis result
              </CardDescription>
            </CardContent>
          </Card>

          <Card className="bg-card/30 backdrop-blur-sm border-border/50">
            <CardHeader>
              <CardTitle className="flex items-center gap-2 text-lg">
                <Sparkles className="h-5 w-5 text-primary" />
                Natural Language
              </CardTitle>
            </CardHeader>
            <CardContent>
              <CardDescription>
                Ask questions in plain English - no complex syntax required
              </CardDescription>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
};

export default Index;