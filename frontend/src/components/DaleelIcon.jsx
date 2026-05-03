export default function DaleelIcon({ size = 32, className }) {
  return (
    <svg
      width={size}
      height={size}
      viewBox="0 0 24 24"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
      className={className}
    >
      <circle cx="12" cy="12" r="12" fill="currentColor" />
      {/* Left page */}
      <path
        d="M12 8 Q9 7 6 7.5 L5.5 16.5 Q8.5 16 12 17"
        stroke="white"
        strokeWidth="1.5"
        strokeLinecap="round"
        strokeLinejoin="round"
      />
      {/* Right page */}
      <path
        d="M12 8 Q15 7 18 7.5 L18.5 16.5 Q15.5 16 12 17"
        stroke="white"
        strokeWidth="1.5"
        strokeLinecap="round"
        strokeLinejoin="round"
      />
      {/* Spine */}
      <line x1="12" y1="8" x2="12" y2="17" stroke="white" strokeWidth="1.5" strokeLinecap="round" />
    </svg>
  )
}
