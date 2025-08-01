import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { 
  Database, 
  Cpu, 
  Zap, 
  Activity,
  CheckCircle2,
  AlertTriangle,
  XCircle
} from 'lucide-react';

interface SystemStatusProps {
  hasDocument: boolean;
  isProcessing: boolean;
  lastQueryTime?: number;
  tokensUsed?: number;
}

export const SystemStatus = ({ hasDocument, isProcessing, lastQueryTime, tokensUsed }: SystemStatusProps) => {
  const getSystemStatus = () => {
    if (isProcessing) return { status: 'processing', icon: Activity, color: 'text-warning' };
    if (hasDocument) return { status: 'ready', icon: CheckCircle2, color: 'text-success' };
    return { status: 'waiting', icon: AlertTriangle, color: 'text-neutral' };
  };

  const { status, icon: StatusIcon, color } = getSystemStatus();

  return (
    <Card className="bg-card/30 backdrop-blur-sm border-border/50">
      <CardHeader className="pb-3">
        <CardTitle className="text-lg flex items-center gap-2">
          <StatusIcon className={`h-5 w-5 ${color} ${isProcessing ? 'animate-pulse' : ''}`} />
          System Status
        </CardTitle>
      </CardHeader>
      <CardContent className="space-y-4">
        <div className="grid grid-cols-1 gap-3">
          {/* Document Status */}
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <Database className="h-4 w-4 text-muted-foreground" />
              <span className="text-sm">Document</span>
            </div>
            <Badge variant={hasDocument ? "default" : "secondary"}>
              {hasDocument ? "Loaded" : "None"}
            </Badge>
          </div>

          {/* Processing Status */}
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <Cpu className="h-4 w-4 text-muted-foreground" />
              <span className="text-sm">Analysis</span>
            </div>
            <Badge variant={isProcessing ? "default" : "secondary"}>
              {isProcessing ? "Processing" : "Idle"}
            </Badge>
          </div>

          {/* Performance Metrics */}
          {lastQueryTime && (
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2">
                <Zap className="h-4 w-4 text-muted-foreground" />
                <span className="text-sm">Last Query</span>
              </div>
              <Badge variant="outline">
                {lastQueryTime}s
              </Badge>
            </div>
          )}
        </div>

        {/* Status Description */}
        <div className="pt-3 border-t border-border/30">
          <p className="text-xs text-muted-foreground">
            {status === 'waiting' && "Upload a document to begin analysis"}
            {status === 'ready' && "Ready to process queries"}
            {status === 'processing' && "Processing your query..."}
          </p>
        </div>
      </CardContent>
    </Card>
  );
};