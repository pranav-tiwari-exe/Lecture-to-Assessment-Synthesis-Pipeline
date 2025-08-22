"use client";
import assets from '@/assets/assets'
import { motion } from 'framer-motion'
import { useRouter } from 'next/navigation';

const Header = () => {

    const router = useRouter();

    return (
        <motion.div className='flex flex-col justify-center items-center text-center my-10'
            initial={{ opacity: 0.2, y: 100 }}
            transition={{ duration: 1 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}>

            <motion.div className='text-stone-500 inline-flex items-center gap-2 bg-white px-6 py-1 rounded-full border border-neutral-500'
                initial={{ opacity: 0, y: -20 }}
                transition={{ duration: 0.8, delay: 0.2 }}
                whileInView={{ opacity: 1, y: 0 }} viewport={{ once: true }}>
                <p>Best Transcript to Questions generator</p>
                <img src={assets.lightMode} alt='' />
            </motion.div>

            <motion.h1 className='text-4xl max-w-[300px] sm:text-7xl sm:max-w-[590px] mx-auto mt-10 text-center'>Turn Transcript to <span className='text-orange-600'
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ delay: 0.4, duration: 2 }}>Questions</span>, in seconds</motion.h1>

            <p className='text-center max-w-xl mx-auto mt-5'
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.6, duration: 0.8 }}>Unlock a world of knowledge with our AI-powered question-answer generator. 💡 Simply ask a question, and our advanced AI will instantly provide a clear, concise, and accurate answer drawn from a vast database of information. Whether you're a student preparing for an exam, a professional researching a topic, or just a curious mind seeking quick facts—our tool makes it effortless to get reliable answers in seconds, transforming the way you learn and work.</p>

            <motion.button className='sm:text-lg text-white bg-black w-auto mt-8 px-12 py-2.5 flex items-center gap-2 rounded-full'
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ default: { duration: 0.5 }, opacity: { delay: 0.8, duration: 1 } }}
                onClick={() => { router.push('/generate') }}>
                Generate Questions
                <img src={assets.star_group} className='h-6'></img>
            </motion.button>


            <motion.p
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ delay: 1.2, duration: 0.8 }}
                className='mt-2 text-neutral-600'> Generated Questions from myQ</motion.p>

        </motion.div>
    )
}

export default Header
