import React from 'react';
import axios from 'axios';
import ReactTable from 'react-table';
import 'react-table/react-table.css'


export default class Player extends React.Component {
    constructor() {
        super();
        this.state = { info: {} }

    }

    componentDidMount() {
        axios.get('http://localhost:5000/player_batting?pid=jared-w-5c8bc0ac3dec1da9b900000d&sid=ferda-baseball-club-5c86c0ac3df30cdf60000001')
            .then(res => {
                for (let game of res.data.games) {
                    game.Date = new Date(game.Date).toISOString().substring(0, 10);
                }
                this.setState({info: res.data})
            })
            .catch(err => {
                console.log(err);
            })
    }

    render() {
        // const player_image = require(`../../public/player_images/${this.props.id}.png`);

        const data = this.state.info.games;
        const columns = [{
            Header: 'Date',
            accessor: 'Date'
        }, {
            Header: 'AB',
            accessor: 'AB',
        }, {
            Header: 'PA',
            accessor: 'PA',
        }, {
            Header: 'AVG',
            accessor: 'AVG',
        }, {
            Header: 'OBP',
            accessor: 'OBP',
        }, {
            Header: 'SLG',
            accessor: 'SLG',
        }, {
            Header: 'OPS',
            accessor: 'OPS',
        }];

        return <div>
            <div style={style} class="container">
                {this.state.info.name}
                <ReactTable
                data={data}
                columns={columns} />
            </div>
            
        </div>
    }
}

const style = {
    padding: "10px",
    fontFamily: "Arial",
    fontSize: "12px"
};

const player_image_style = {
    width: "1",
    height: "1"  
};
