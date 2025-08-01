import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Accordion, AccordionContent, AccordionItem, AccordionTrigger } from '@/components/ui/accordion';
import { Progress } from '@/components/ui/progress';
import { 
  CheckCircle2, 
  XCircle, 
  AlertTriangle, 
  FileText, 
  Brain, 
  Lightbulb,
  Scale,
  Clock,
  ExternalLink
} from 'lucide-react';

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

interface ResultsDisplayProps {
  result: QueryResult | null;
  isLoading: boolean;
}

export const ResultsDisplay = ({ result, isLoading }: ResultsDisplayProps) => {
  if (isLoading) {
    return (
      <Card className="bg-card/50 backdrop-blur-sm border-border/50 shadow-glass">
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Brain className="h-5 w-5 text-primary animate-pulse-soft" />
            Processing Query
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="space-y-3">
            <div className="flex items-center gap-2">
              <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-primary" />
              <span className="text-sm text-muted-foreground">Processing document...</span>
            </div>
            <div className="flex items-center gap-2">
              <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-primary" />
              <span className="text-sm text-muted-foreground">Analyzing content...</span>
            </div>
            <div className="flex items-center gap-2">
              <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-primary" />
              <span className="text-sm text-muted-foreground">Generating analysis...</span>
            </div>
          </div>
        </CardContent>
      </Card>
    );
  }

  if (!result) {
    return (
      <Card className="bg-card/50 backdrop-blur-sm border-border/50 shadow-glass">
        <CardContent className="flex items-center justify-center h-32">
          <div className="text-center space-y-2">
            <FileText className="h-8 w-8 mx-auto text-muted-foreground" />
            <p className="text-sm text-muted-foreground">
              Submit a query to see intelligent analysis results
            </p>
          </div>
        </CardContent>
      </Card>
    );
  }

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'covered':
        return <CheckCircle2 className="h-5 w-5 text-success" />;
      case 'not_covered':
        return <XCircle className="h-5 w-5 text-destructive" />;
      case 'conditional':
        return <AlertTriangle className="h-5 w-5 text-warning" />;
      default:
        return <AlertTriangle className="h-5 w-5 text-neutral" />;
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'covered':
        return 'bg-success/10 text-success border-success/20';
      case 'not_covered':
        return 'bg-destructive/10 text-destructive border-destructive/20';
      case 'conditional':
        return 'bg-warning/10 text-warning border-warning/20';
      default:
        return 'bg-neutral/10 text-neutral border-neutral/20';
    }
  };

  return (
    <div className="space-y-6">
      {/* Main Answer */}
      <Card className="bg-card/50 backdrop-blur-sm border-border/50 shadow-glass">
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            {getStatusIcon(result.status)}
            Analysis Result
            <Badge variant="secondary" className="ml-auto">
              {Math.round(result.confidence * 100)}% confident
            </Badge>
          </CardTitle>
          <CardDescription>
            Query: "{result.query}"
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className={`p-4 rounded-lg border ${getStatusColor(result.status)}`}>
            <p className="font-medium">{result.answer}</p>
          </div>

          {result.conditions.length > 0 && (
            <div className="space-y-2">
              <h4 className="font-semibold flex items-center gap-2">
                <Scale className="h-4 w-4" />
                Conditions & Requirements
              </h4>
              <ul className="space-y-2">
                {result.conditions.map((condition, index) => (
                  <li key={index} className="flex items-start gap-2 p-2 bg-secondary/30 rounded">
                    <div className="w-1.5 h-1.5 bg-primary rounded-full mt-2 flex-shrink-0" />
                    <span className="text-sm">{condition}</span>
                  </li>
                ))}
              </ul>
            </div>
          )}

          {/* Confidence and Performance Metrics */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 pt-4 border-t border-border">
            <div className="text-center">
              <div className="text-2xl font-bold text-primary">{Math.round(result.confidence * 100)}%</div>
              <div className="text-xs text-muted-foreground">Confidence</div>
            </div>
            {result.processing_time && (
              <div className="text-center">
                <div className="text-2xl font-bold text-primary">{result.processing_time}s</div>
                <div className="text-xs text-muted-foreground">Processing Time</div>
              </div>
            )}
            {result.token_usage && (
              <div className="text-center">
                <div className="text-2xl font-bold text-primary">{result.token_usage}</div>
                <div className="text-xs text-muted-foreground">Tokens Used</div>
              </div>
            )}
          </div>
        </CardContent>
      </Card>

      {/* Detailed Analysis */}
      <Card className="bg-card/50 backdrop-blur-sm border-border/50 shadow-glass">
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Lightbulb className="h-5 w-5 text-primary" />
            Explainable Analysis
          </CardTitle>
        </CardHeader>
        <CardContent>
          <Accordion type="single" collapsible className="w-full">
            <AccordionItem value="rationale">
              <AccordionTrigger className="text-left">
                Decision Rationale
              </AccordionTrigger>
              <AccordionContent className="space-y-3">
                <p className="text-sm leading-relaxed">{result.decision_rationale}</p>
              </AccordionContent>
            </AccordionItem>

            <AccordionItem value="evidence">
              <AccordionTrigger className="text-left">
                Supporting Evidence ({result.evidence.length} clauses)
              </AccordionTrigger>
              <AccordionContent className="space-y-4">
                {result.evidence.map((evidence, index) => (
                  <div key={index} className="p-4 bg-secondary/20 rounded-lg border border-border/30">
                    <div className="flex items-center justify-between mb-2">
                      <div className="flex items-center gap-2">
                        <Badge variant="outline" className="text-xs">
                          {evidence.clause_id}
                        </Badge>
                        <Badge variant="secondary" className="text-xs">
                          {Math.round(evidence.similarity_score * 100)}% match
                        </Badge>
                      </div>
                      <div className="flex items-center gap-1 text-xs text-muted-foreground">
                        <FileText className="h-3 w-3" />
                        {evidence.source}
                      </div>
                    </div>
                    <blockquote className="text-sm italic border-l-2 border-primary pl-3 py-1">
                      "{evidence.text}"
                    </blockquote>
                    {evidence.section && (
                      <p className="text-xs text-muted-foreground mt-2">
                        Section: {evidence.section}
                      </p>
                    )}
                  </div>
                ))}
              </AccordionContent>
            </AccordionItem>
          </Accordion>
        </CardContent>
      </Card>
    </div>
  );
};