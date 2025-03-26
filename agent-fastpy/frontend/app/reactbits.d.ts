declare module 'reactbits' {
  export const Button: React.FC<{ color: string; children?: React.ReactNode; className?: string }>;
  export const Input: React.FC<{ placeholder: string; className?: string }>;
  export const Textarea: React.FC<{ placeholder: string; className?: string }>;
}
