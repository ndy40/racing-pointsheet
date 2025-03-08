import {Link, Outlet} from "react-router";
import RaceToolbar from "~/routes/races/components/race_toolbar";


export default function RacesLayout() {
    return <>
        <RaceToolbar/>
        <section id="content">
            <Outlet />
        </section>
    </>
}