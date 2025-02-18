import {LargeRaceCard} from "@/components/race_card";


interface EventDetails {
    title: string
    starts_at: Date
    ends_at: Date
    status: string
    track: string
}


function EventCard() {
    return <LargeRaceCard>
        <>
        <h1 className="text-xl text-gray-700">Event title here</h1>
        <div id="event_details" className="flex flex-col mt-2">
            <div className="flex justify-between">
                <div id="date" className="flex gap-2"><span className="material-icons-two-tone">event_available</span> 4th Jan. 20:00 GMT</div>
                <div id="track" className="flex gap-2"><span className="material-icons-outlined">add_road</span> Road America</div>
            </div>
            <div className="flex justify-start">
                <div id="time" className="flex gap-2"><span className="material-icons-outlined">schedule</span> 1h 30m</div>
            </div>
            <div className="flex justify-between">
                <div id="date" className="flex gap-2"><span
                    className="material-icons-outlined">sports_motorsports</span> 10/20
                </div>
                <button className="text-gray-600 border border-gray-400 bg-transparent rounded-lg px-4 flex text-center gap-2 hover:ring-1 hover:ring-gray-600"><span className="material-icons-outlined">flag</span> Race</button>
            </div>

        </div>
        </>
    </LargeRaceCard>
}


export default EventCard;
