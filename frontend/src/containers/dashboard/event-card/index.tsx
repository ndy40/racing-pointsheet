import {LargeRaceCard} from "@/components/race_card";


function EventCard() {
    return <LargeRaceCard>
        <>
        <div className="mb-10"><h1 className="font-medium text-gray-700">Event title here</h1></div>
        <div id="event_details" className="flex flex-col mt-2">
            <div className="flex justify-between">
                <div id="date" className="flex gap-2"><span className="material-icons-two-tone">event_available</span> 4th Jan. 20:00 GMT</div>
                <div id="track" className="flex gap-2"><span className="material-icons-outlined">add_road</span> Road America</div>
            </div>
            <div className="flex justify-start">
                <div id="time" className="flex gap-2"><span className="material-icons-outlined">schedule</span> 1h 30m</div>
            </div>
            <div className="flex justify-between">
                <div id="date" className="flex gap-2"><span className="material-icons-outlined">sports_motorsports</span> 10/20</div>
                <a  className="pb-10 rounded-sm bg-green-500"><span className="material-icons-outlined">flag</span>Race</a>
            </div>
        </div>
        </>
    </LargeRaceCard>
}


export default EventCard;
