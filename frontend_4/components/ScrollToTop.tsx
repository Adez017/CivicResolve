"use client";

// import useeffect and usepathname
import { useEffect } from "react";
import { usePathname } from "next/navigation";

// scroll to top on pathname change
export default function ScrollToTop() {
    const pathname = usePathname();

    useEffect(() => {
        window.scrollTo({ top: 0, left: 0 });
    }, [pathname]);

    return null;
}