<template>
    <div>
        <form @submit.prevent="fetch_remote_data">
            
            <div class="form-group">
                <h2> Weather Data </h2>
                <p> Please fill in the form and use the submit button to load data.</p>
                <label for="">Location</label>
                <br>
                <!-- The input field for the location, bound to the data_inputted.location property -->
                <input class="form-control rounded" v-model="form_input.location" type="text" required />
            </div>
            
            <div class="form-group">
                <label for="">Start Date</label>
                <br>
                <!-- The input field for the start date, bound to the data_inputted.start_dt property -->
                <input class="form-control rounded" type="date" v-model="form_input.start_dt" required />
            </div>
            
            <div class="form-group">
                <label for="">End Date</label>
                <br>
                
                <input class="form-control rounded" type="date" v-model="form_input.end_dt" required />
            </div>
            <br>
            <div>
                <button class="btn btn-danger" type="submit">Submit</button>
            </div>
        </form>
        <br /><br />

        <div v-if = "dataLoaded">
            <Bar :data="chart_data" :options="chart_options" />
        </div>

        <div v-if = "dataLoaded">
            <hr>
            <h5> Weather Data in a Table</h5>
            <table class="table">
                <thead>
                    <tr>
                        <th v-for="adate in keys">{{ adate }}</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td v-for="atemp in values">{{ atemp }}</td>
                    </tr>
                </tbody>
            </table>            
        </div>

    </div>
</template>

<style>
table, th, td {
  border: 1px solid black;
  border-collapse: collapse;
}
</style>

<script>

import axios from "axios";

import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  BarElement,
  CategoryScale,
  LinearScale
} from 'chart.js'
import { Bar } from 'vue-chartjs'

ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend)

export default {
    components: {
        // Line
        //BarChart: Bar,
        Bar,
    },
    
    data() {
        return {
            form_input: {
                start_dt: "",
                end_dt: "",
                location: "",
            },

            chart_options: {
                responsive: true,
                maintainAspectRatio: true,
                scales: {
                    x: {
                        title: {
                            display: true,
                            text: "Time",
                        },
                    },
                    y: {
                        title: {
                            display: true,
                            text: "Temperature (F)",
                        },
                    },
                },
            },

            chart_data: {
                labels: [], 
                datasets: [
                    {
                        label: "Average Temperature", 
                        backgroundColor: "#f87979", 
                        data: [], 
                    },
                ],
            },
            dataLoaded: false,
            
            keys: [],
            values: [],
            // daily_temp: {},
        };
    },

    methods: {
        // https://rapidapi.com/weatherapi/api/weatherapi-com/
        async fetch_remote_data() {
            const options = {
                method: 'GET',
                url: 'https://weatherapi-com.p.rapidapi.com/history.json',
                params: {
                    q: this.form_input.location,
                    dt: this.form_input.start_dt,
                    end_dt: this.form_input.end_dt,
                    lang: 'en'
                },
                headers: {
                    'X-RapidAPI-Key': '6c6f790650msh5ce4da2fced77a7p1b1776jsn247d9f531b74',
                    'X-RapidAPI-Host': 'weatherapi-com.p.rapidapi.com'
                }
            };
            
            try {
                await axios.request(options).then((resp) => {
                    // this.keys.forEach((element, index) => {
                    //    this.daily_temp[element] = this.values[index];
                    // });
                    // console.log(this.daily_temp);

                    const w_data = resp.data.forecast.forecastday; 
                    this.keys = w_data.map((item) => item.date);
                    this.values = w_data.map((item) => item.day.avgtemp_f);

                    
                    this.chart_data = {
                        labels: this.keys, 
                        datasets: [
                            {
                                label: "Average Temperature", 
                                backgroundColor: "#f87979", 
                                data: this.values, 
                            },
                        ],
                    },
                    
                    this.dataLoaded = true;
                })
            } catch (error) {
                console.error(error);
            }
            
        }
    },
}

</script>
