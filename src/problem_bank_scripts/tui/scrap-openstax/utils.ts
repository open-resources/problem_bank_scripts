import * as cheerio from 'cheerio';

export async function fetchScrap(url: string) {
    const res = await retry(async () => await fetch(url, { cache: 'no-store' }), {
        times: 10
    });
    await sleep(10000)
    const body = await res.text()
    const $ = cheerio.load(body);
    return $
}

export const sleep = (ms = 0) => new Promise((resolve) => setTimeout(resolve, ms))

export const retry = async <T>(
    fn: () => Promise<T> | T,
    { times }: { times: number },
    curCount = 0
): Promise<T> => {
    try {
        return await fn()
    } catch (error) {
        if (times <= 0) {
            throw error
        }

        await sleep(50 * Math.pow(2, curCount))
        return retry(fn, { times: times - 1 }, curCount + 1)
    }
}