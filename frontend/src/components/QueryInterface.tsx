import { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Textarea } from '@/components/ui/textarea';
import { Label } from '@/components/ui/label';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Search, Sparkles, Clock, Brain } from 'lucide-react';

interface QueryInterfaceProps {
  onQuerySubmit: (query: string) => void;
  isProcessing: boolean;
  hasDocument: boolean;
}

const SAMPLE_QUERIES = [
  "What is covered under this policy?",
  "What are the exclusions and limitations?",
  "What conditions apply to this coverage?",
  "What is the waiting period for pre-existing conditions?",
  "What are the claim submission requirements?"
];

export const QueryInterface = ({ onQuerySubmit, isProcessing, hasDocument }: QueryInterfaceProps) => {
  const [query, setQuery] = useState('');

  const handleSubmit = () => {
    if (!query.trim()) return;
    onQuerySubmit(query);
  };

  const handleSampleQuery = (sampleQuery: string) => {
    setQuery(sampleQuery);
  };

  return (
    <Card className="bg-card/50 backdrop-blur-sm border-border/50 shadow-glass">
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <Brain className="h-5 w-5 text-primary" />
          Intelligent Query
        </CardTitle>
        <CardDescription>
          Ask natural language questions about your document
        </CardDescription>
      </CardHeader>
      <CardContent className="space-y-6">
        <div className="space-y-2">
          <Label htmlFor="query">Your Question</Label>
          <Textarea
            id="query"
            placeholder="e.g., Does this policy cover knee surgery, and what are the conditions?"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            className="min-h-[100px] bg-background/50 resize-none"
            disabled={!hasDocument}
          />
        </div>

        <Button 
          onClick={handleSubmit}
          disabled={!hasDocument || !query.trim() || isProcessing}
          className="w-full bg-gradient-primary hover:opacity-90 transition-smooth"
        >
          {isProcessing ? (
            <>
              <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2" />
              Processing Query...
            </>
          ) : (
            <>
              <Search className="h-4 w-4 mr-2" />
              Analyze Document
            </>
          )}
        </Button>

        {!hasDocument && (
          <div className="p-4 bg-warning/10 rounded-lg border border-warning/20">
            <p className="text-sm text-warning font-medium">
              Please upload a document first to start querying
            </p>
          </div>
        )}

        <div className="space-y-3">
          <div className="flex items-center gap-2">
            <Sparkles className="h-4 w-4 text-muted-foreground" />
            <span className="text-sm font-medium text-muted-foreground">Sample Questions</span>
          </div>
          <div className="space-y-2">
            {SAMPLE_QUERIES.map((sampleQuery, index) => (
              <button
                key={index}
                onClick={() => handleSampleQuery(sampleQuery)}
                disabled={!hasDocument}
                className="w-full text-left p-3 text-sm bg-secondary/50 hover:bg-secondary/80 rounded-lg transition-smooth border border-border/30 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {sampleQuery}
              </button>
            ))}
          </div>
        </div>

        {hasDocument && (
          <div className="flex items-center gap-2 p-3 bg-info/10 rounded-lg border border-info/20">
            <Clock className="h-4 w-4 text-info" />
            <span className="text-sm text-info">
              AI analysis in progress...
            </span>
          </div>
        )}
      </CardContent>
    </Card>
  );
};