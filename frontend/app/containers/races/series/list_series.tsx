import {Table, TableBody, TableCaption, TableCell, TableHead, TableHeader, TableRow} from "~/components/ui/table";


type Series = {
    id: string
    title: string
    status: string
}


export function SeriesRow({series}: {series: Series}) {
    return <TableRow key={series.id}>
        <TableCell>{series.title}</TableCell>
        <TableCell className="capitalize">{series.status}</TableCell>
    </TableRow>;
}


export function ListSeriesTable({series}: {series: Series[]}) {
    return <>
        <Table>
            <TableCaption>List of events by status</TableCaption>
            <TableHeader className="bg-gray-700">
                <TableRow className="text-gray-600">
                    <TableHead className="w-1/4 text-gray-300">Series</TableHead>
                    <TableHead className="text-gray-300">Status</TableHead>
                    <TableHead className="text-gray-300">Starts On</TableHead>
                    <TableHead className="text-gray-300">Ends On</TableHead>
                    <TableHead className="text-gray-300">Action</TableHead>
                </TableRow>
            </TableHeader>
            <TableBody>
                {series?.map((item) => <SeriesRow series={item}/>) }
            </TableBody>
        </Table>

    </>
}