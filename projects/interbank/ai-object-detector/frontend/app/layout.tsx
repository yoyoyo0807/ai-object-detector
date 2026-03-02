export const metadata = {
  title: 'AI Object Detector',
  description: 'YOLOv11 powered object detection',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="ja">
      <body>{children}</body>
    </html>
  )
}