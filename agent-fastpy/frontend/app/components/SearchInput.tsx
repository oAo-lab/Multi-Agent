interface SearchInputProps {
  placeholder: string;
  value: string;
  onChange: (value: string) => void;
}

export default function SearchInput({ 
  placeholder,
  value,
  onChange
}: SearchInputProps) {
  return (
    <div className="input-group">
      <input
        required
        type="text"
        value={value}
        onChange={(e) => onChange(e.target.value)}
        className="input"
        placeholder=" "
      />
      <label className="user-label">{placeholder}</label>
    </div>
  );
}
