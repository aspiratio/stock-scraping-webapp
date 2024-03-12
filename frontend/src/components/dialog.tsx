import { Dialog } from "@headlessui/react"

type Props = {
  isOpen: boolean
  handleOpen: () => void
  onClickSubmit: () => void
  children: React.ReactNode
}

const ConfirmDialog = ({
  isOpen,
  handleOpen,
  onClickSubmit,
  children,
}: Props) => {
  return (
    <Dialog open={isOpen} onClose={handleOpen} className="relative z-50">
      <div className="fixed inset-0 bg-black/30" aria-hidden="true">
        <div className="fixed inset-0 flex w-screen items-center justify-center">
          <Dialog.Panel className="w-full max-w-sm rounded bg-gray-50 p-8">
            <Dialog.Title className="text-gray-700">{children}</Dialog.Title>
            <div className="flex justify-center gap-4 mt-4">
              <button
                onClick={handleOpen}
                className="inline-flex justify-center rounded-md border border-transparent bg-red-100 px-4 py-2 text-md font-medium text-red-900 hover:bg-red-200 focus:outline-none focus-visible:ring-2 focus-visible:ring-red-500 focus-visible:ring-offset-2"
              >
                Cancel
              </button>
              <button
                onClick={onClickSubmit}
                className="inline-flex justify-center rounded-md border border-transparent bg-blue-100 px-4 py-2 text-md font-medium text-blue-900 hover:bg-blue-200 focus:outline-none focus-visible:ring-2 focus-visible:ring-blue-500 focus-visible:ring-offset-2"
              >
                OK
              </button>
            </div>
          </Dialog.Panel>
        </div>
      </div>
    </Dialog>
  )
}

export default ConfirmDialog
