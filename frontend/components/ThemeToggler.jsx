'use client';
import { useTheme } from 'next-themes'
import { useEffect, useState } from 'react'
import assets from '../assets/assets'
import Image from 'next/image';

const ThemeToggler = () => {

    const [mounted, setMounted] = useState(false);
    const {setTheme, resolvedTheme} = useTheme()

    useEffect(() => setMounted(true), [])

    if (!mounted) return <p className='text-sm bg-gray-700'>Loading...</p>

    return (
        resolvedTheme === 'dark' ?
            (<button onClick={() => setTheme('light')}>
                <Image src={assets.lightMode} alt='light_mode_icon' width={26}/>
            </button>) :
            (<button onClick={() => setTheme('dark')}>
                <Image src={assets.darkMode} alt='dark_mode_icon' width={26}/>
            </button>)
    )
}

export default ThemeToggler