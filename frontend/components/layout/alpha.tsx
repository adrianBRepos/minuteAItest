import Link from 'next/link'

export function Alpha() {
  return (
    <div className="text-sm">
      <div className="flex gap-2 px-6">
        <p>
          For advice and support visit our page on the{' '}
          <Link
            href="https://cccandpcc.sharepoint.com/sites/ICT/SitePages/Minute-AI-transcription-tool.aspx?TeamsCID=9462b575-df48-4956-89a1-553717386789&linkOpenTime=1781087220107"
            className="a inline text-blue-600 underline underline-offset-1 hover:text-blue-800 hover:decoration-3 active:bg-yellow-400 active:text-black"
            target="_blank"
            rel="noopener noreferrer"
          >
            intranet
          </Link>
        </p>
      </div>
    </div>
  )
}
