"use client"

import {useState} from "react";


export function Tabs() {
    const [activeTab, setActiveTab] = useState(0)
    
    const tabs = [
        {"title": "Upcoming", data: []},
        {"title": "Available", data: []},
        {"title": "Series Standing", data: []},
    ]
    
    return <>
        <div className="w-auto bg-white rounded-lg p-4 shadow-lg">
            <div id="tab-heading" className="flex border-b border-gray-200">
                { tabs.map(
                    (item, idx) => 
                        <button key={idx} id={idx.toString()} className={"p-4 py-2 gray-600 border-b-2 border-transparent focus:outline-none focus:border-gray-400 " + (activeTab == idx  ? 'border-gray-400': '')}
                                onClick={() => setActiveTab(idx)}
                        >
                    {item.title}
                </button>)}
            </div>
            <div id="tab-content">
                {tabs.map((item, idx) => <div key={idx} id={`idx.toString()`} className={"p-4 tab-content " + (activeTab == idx ? '' : 'hidden')}>
                    Tab {idx}
                    </div>
                )}
            </div>
        </div>
    </>
}
