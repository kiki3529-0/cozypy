#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
This example can be run safely as it won't change anything in your box configuration
'''

import asyncio
import logging
import os

from cozypy import CozytouchClient

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)

username = os.getenv("COZYPY_USERNAME")
password = os.getenv("COZYPY_PASSWORD")

client = CozytouchClient(username, password)


async def async_demo():
    async def device_info(device):
        logger.info("\t Name:{}".format(device.name))
        logger.info("\t Client:{}".format(device.client))
        logger.info("\t Creation Time:{}".format(device.creationTime))
        logger.info("\t Device url:{}".format(device.device_url))
        logger.info("\t\t Id:{}".format(device.id))
        logger.info("\t\t Place:{}".format(device.place))
        logger.info("\t\t Gateway:{}".format(device.gateway))
        logger.info("\t\t Suported states:")
        for state in device.supported_states:
            logger.info("\t\t\t {}".format(state))
        logger.info("\t\t States value:")
        for state in device.supported_states:
            logger.info("\t\t\t {} {}".format(state.value, device.get_state(state)))
        logger.info("\t\t Is on: {}".format(device.is_on))
        if hasattr(device, "operating_mode"):
            logger.info("\t\t Operating mode:{}".format(device.operating_mode))
        if hasattr(device, "sensors") and len(device.sensors) > 0:
            logger.info("\t\t Sensors")
            for sensor in device.sensors:
                logger.info("\t\t\t Id:{}".format(sensor.id))
                logger.info("\t\t\t Parent:{}".format(sensor.parent))
                logger.info("\t\t\t Name:{}".format(sensor.name))
                logger.info("\t\t\t Type: {}".format(sensor.widget))
                logger.info("\t\t\t States value:")
                for sensor_state in sensor.states:
                    logger.info("\t\t\t\t {name}: {value}".format(name=sensor_state["name"], value=sensor_state["value"]))

    setup = await client.async_get_setup()
    logger.info("### PLACES ###")
    for place in setup.places:
        logger.info(place)

    logger.info("### WATER HEATERS ###")
    for water_heater in setup.water_heaters:
        logger.info(water_heater.id)
        await device_info(water_heater)

    logger.info("### HEATERS ###")
    for heater in setup.heaters:
        logger.info(heater.id)
        await device_info(heater)

    logger.info("### PODS ###")
    for pod in setup.pods:
        logger.info(pod.id)
        await device_info(pod)

    logger.info("### GATEWAYS ###")
    for gw in setup.gateways:
        logger.debug(gw.id)
        logger.debug(gw.is_on)
        logger.debug(gw.version)
        logger.debug(gw.status)
        logger.info("Place:{}".format(gw.place))

loop = asyncio.get_event_loop()
loop.run_until_complete(async_demo())
loop.close()
