import Navbar from '@/components/Navbar'
import VideoInput from '@/components/VideoInput'
import React from 'react'

const Page = () => {
  return (
    <div className="sm:mx-0 md:mx-10 lg:mx-20 xl:mx-40">
      <Navbar />
      <VideoInput/>
    </div>
  )
}

export default Page