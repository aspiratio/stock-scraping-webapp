type Props = {
  className?: string
  onClick?: () => void
  disabled?: boolean
  type: "submit" | "reset" | "button" | undefined
  children: React.ReactNode
}

const Button = ({ className, onClick, disabled, type, children }: Props) => {
  return (
    <button
      className={`bg-orange-500 hover:bg-orange-600 rounded-md px-4 py-2 shadow-md active:shadow-none shadow-gray-800 active:relative active:top-1 ${className}`}
      onClick={onClick}
      disabled={disabled}
      type={type}
    >
      {children}
    </button>
  )
}

export default Button
