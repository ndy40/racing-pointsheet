"use client"

import {ReactElement, ReactNode, useState} from "react";


interface TabItemProps {
    title: string,
    label: string,
    children: ReactNode
}

export function TabItem(props: TabItemProps): ReactElement {
    return <>{props.children}</>
}

export function Tabs({children}: {children: ReactElement<TabItemProps>[] }) {
    const [activeTab, setActiveTab] = useState(children[0].props.label)
    const tabContent = children.filter(child => child.props.label === activeTab)
    
    return <>
        <div className="w-auto bg-white rounded-lg p-4 shadow-lg">
            <div id="tab-heading" className="flex border-b border-gray-200">
                { children.map(
                    (child, idx) => 
                        <button key={idx} id={child.props.label} className={"p-4 py-2 gray-600 border-b-2 border-transparent focus:outline-none focus:border-gray-400 " + (activeTab == child.props.label  ? 'border-gray-400': '')}
                                onClick={() => setActiveTab(child.props.label)}
                        >
                    {child.props.title}
                </button>)}
            </div>
            <div id="tab-content" className="p-4">
                {tabContent}
            </div>
        </div>
    </>;
}



