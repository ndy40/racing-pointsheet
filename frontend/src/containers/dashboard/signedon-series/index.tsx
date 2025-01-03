import RaceCard from "@/components/race_card";


function SeriesSignUpCard() {
    return (
        <RaceCard>
            <>
                <div className="flex flex-col justify-between">
                    <h2 className="text-sm font-bold">On Going Series</h2>
                    <div className="flex justify-between py-3">
                        <span className="text-gray-500 text-4xl font-medium">2 / 4</span>
                        <div className="flex py-2">
                            <span className="material-icons-outlined">tour</span>
                        </div>

                    </div>
                </div>
            </>
        </RaceCard>
    );
}

export default SeriesSignUpCard;
