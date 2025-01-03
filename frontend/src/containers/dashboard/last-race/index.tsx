import {RaceCard} from "@/components/race_card";


function LastRaceCard(){
    return <RaceCard>
        <>
        <h2 className="text-sm font-bold">Last Race</h2>
        <div className="flex py-3 gap-6 text-xl text-gray-500">
            <div className="text-xl font-medium">
                10/12
            </div>
            <div id="points" className="text-xl">
                Pt: 10
            </div>
        </div>
        <p className="text-gray-800">Laguna Seca</p>
        <p className="text-gray-400">FL: 2.14.333</p>
        </>
    </RaceCard>
}


export default LastRaceCard
