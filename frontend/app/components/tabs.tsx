import {type ReactElement, useState} from "react";


interface TabItemProps {
    title: string,
    label: string,
    children: Element
}

export function TabItem(props: TabItemProps): ReactElement {
    return <>{props.children}</>
}

export function Tabs({children}: {children: ReactElement<typeof TabItem>[]}) {
    const [activeTab, setActiveTab] = useState(children[0].props.label)
    const tabContent = children.filter(child => child.props.label === activeTab)

    return <>
        <div className="w-auto bg-white rounded-lg p-4 shadow-gray-200 shadow-sm">
            <div id="tab-heading" className="flex border-b border-gray-100 text-gray-700">
                { children.map(
                    (child, idx) =>
                        <button
                            key={idx} id={child.props.label}
                            className={"p-4 py-2 gray-800 border-b-2 border-transparent focus:outline-none focus:border-gray-400 " + (activeTab === child.props.label  ? 'border-gray-400': '')}
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
